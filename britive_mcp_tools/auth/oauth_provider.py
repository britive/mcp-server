from britive_mcp_tools.auth.auth_provider import AuthProvider
from britive.britive import Britive
from fastmcp import Context
from britive_mcp_tools.utils import get_env_or_raise

from fastmcp.server.auth import RemoteAuthProvider
from fastmcp.server.auth.providers.jwt import JWTVerifier
from pydantic import AnyHttpUrl
import os

class OAuthProvider(AuthProvider):
    """
    Auth provider that retrieves the OAuth token dynamically from the request context (ctx).
    Tenant DNS is passed at initialization.
    """

    def __init__(self, tenant: str):
        self.tenant = tenant
        self.oauth2_domain = os.environ.get(
            "OAUTH2_DOMAIN", 
            f"https://{self.tenant}.britive-app.com/api/auth/sso/oauth2/"
        )
        self.oauth2_audience = os.environ.get("OAUTH2_AUDIENCE", "Britive")
        self.oauth2_issuer = os.environ.get("OAUTH2_ISSUER", "Britive")
        self.resource_server = get_env_or_raise("RESOURCE_SERVER")
        self._ctx: Context = None

    def _get_token(self) -> str:
        """
        Extracts the OAuth token from the Authorization header in the request context.
        """
        if not self._ctx:
            raise RuntimeError("Context not set. Did you specify the provider correctly?")

        try:
            auth_header = self._ctx.get_http_request().headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                raise ValueError(
                "No valid OAuth token found. "
                "Please log in using the OAuth provider before calling this tool."
                )
            return auth_header[7:]
        except RuntimeError:
            # No active request context at all
            raise ValueError(
                "Failed to extract token: No active HTTP request found. "
                "Please log in using OAuth before using this tool."
            )
        except Exception as e:
            raise ValueError(f"Unexpected error while extracting token: {e}")

    def _get_tenant_dns(self) -> str:
        """
        Returns the tenant DNS passed during initialization.
        """
        return self.tenant

    def get_client(self, ctx: Context) -> Britive:
        """
        Retrieves token from context and returns an authenticated Britive client.
        """
        self._ctx = ctx
        token = self._get_token()
        tenant_dns = self._get_tenant_dns()
        client = Britive(tenant=tenant_dns, token=token)

        # Update User-Agent for MCP integration
        user_agent = client.session.headers.get("User-Agent", "")
        client.session.headers.update({"User-Agent": f"Britive MCP Server {user_agent}"})
        return client

    def get_auth(self) -> RemoteAuthProvider:
        token_verifier = JWTVerifier(
            jwks_uri=f'{self.oauth2_domain}keys',
            issuer=self.oauth2_issuer,
            audience=self.oauth2_audience,
        )
        
        auth = RemoteAuthProvider(
            token_verifier=token_verifier,
            authorization_servers=[AnyHttpUrl(self.oauth2_domain)],
            resource_server_url=self.resource_server
        )
        return auth