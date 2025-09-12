import os
from pydantic import AnyHttpUrl
from fastmcp import Context
from fastmcp.server.auth import RemoteAuthProvider
from fastmcp.server.auth.providers.jwt import JWTVerifier
from britive.britive import Britive
from britive_mcp_tools.auth.auth_provider import AuthProvider


class OAuthProvider(AuthProvider):
    """
    Auth provider that dynamically retrieves OAuth tokens from the request context (ctx).
    Tenant DNS is passed during initialization.
    """

    def __init__(self, tenant: str):
        self.tenant = tenant
        self.base_tenant_url = f"https://{tenant}.britive-app.com"

        # OAuth2 settings (env override > default)
        self.oauth2_domain = os.environ.get("OAUTH2_DOMAIN", f"{self.base_tenant_url}/api/auth/sso/oauth2/")
        self.oauth2_audience = os.environ.get("OAUTH2_AUDIENCE", "Britive")
        self.oauth2_issuer = os.environ.get("OAUTH2_ISSUER", "Britive")

        # MCP transport settings
        self.transport_type = "streamable-http"
        self.host = os.environ.get("MCP_HOST", "0.0.0.0")
        self.port = int(os.environ.get("MCP_PORT", 80))
        self.path = os.environ.get("MCP_PATH", "/")

        # Resource server defaults
        scheme = "" if self.host.startswith("http") else "http://"
        host = "127.0.0.1" if self.host == "0.0.0.0" else self.host
        default_url = f"{scheme}{host}:{self.port}{self.path}"
        self.resource_server = os.environ.get("RESOURCE_SERVER", default_url)

        self._ctx: Context | None = None

    def _get_token(self) -> str:
        """Extracts the OAuth token from the Authorization header in the request context."""
        if not self._ctx:
            raise RuntimeError("Context not set. Did you configure the provider correctly?")

        try:
            auth_header = self._ctx.get_http_request().headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                raise ValueError("No valid OAuth token found. Please log in with OAuth first.")
            return auth_header[7:]
        except RuntimeError:
            raise ValueError("No active HTTP request found. Please log in with OAuth before using this tool.")
        except Exception as e:
            raise ValueError(f"Unexpected error while extracting token: {e}")

    def _get_tenant_dns(self) -> str:
        """Returns the tenant DNS passed during initialization."""
        return self.tenant

    def get_client(self, ctx: Context) -> Britive:
        """Retrieves token from context and returns an authenticated Britive client."""
        self._ctx = ctx
        token = self._get_token()
        client = Britive(tenant=self._get_tenant_dns(), token=token)

        # Append MCP identifier to User-Agent
        ua = client.session.headers.get("User-Agent", "")
        client.session.headers.update({"User-Agent": f"Britive MCP Server {ua}"})
        return client

    def get_auth(self) -> RemoteAuthProvider:
        """Returns a RemoteAuthProvider configured for OAuth token verification."""
        verifier = JWTVerifier(
            jwks_uri=f"{self.oauth2_domain}keys",
            issuer=self.oauth2_issuer,
            audience=self.oauth2_audience,
        )
        return RemoteAuthProvider(
            token_verifier=verifier,
            authorization_servers=[AnyHttpUrl(self.oauth2_domain)],
            resource_server_url=self.resource_server,
        )

    def get_runner_params(self) -> dict:
        """Return parameters required to run the MCP server."""
        params = {"transport": self.transport_type}
        if self.transport_type == "streamable-http":
            params.update(host=self.host, port=self.port, path=self.path)
        return params
