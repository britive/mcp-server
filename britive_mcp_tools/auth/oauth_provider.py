from britive_mcp_tools.auth.auth_provider import AuthProvider
from britive.britive import Britive
from fastmcp import Context
from britive_mcp_tools.utils import get_env_or_raise

from fastmcp.server.auth import RemoteAuthProvider
from fastmcp.server.auth.providers.jwt import JWTVerifier
from pydantic import AnyHttpUrl

class OAuthProvider(AuthProvider):
    """
    Auth provider that retrieves the OAuth token dynamically from the request context (ctx).
    Tenant DNS is passed at initialization.
    """

    def __init__(self, tenant: str):
        self.tenant = tenant
        self._ctx: Context = None

    def _get_token(self) -> str:
        """
        Extracts the OAuth token from the Authorization header in the request context.
        """
        if not self._ctx:
            raise RuntimeError("Context not set.")

        try:
            auth_header = self._ctx.get_http_request().headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                raise ValueError("Authorization header is missing or invalid.")
            return auth_header[7:]  # Remove 'Bearer '
        except Exception as e:
            raise ValueError(f"Failed to extract token from context: {e}")

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
        oauth2_domain = get_env_or_raise("OAUTH2_DOMAIN")
        oauth2_audience = get_env_or_raise("OAUTH2_AUDIENCE")
        oauth2_issuer = get_env_or_raise("OAUTH2_ISSUER")
        resource_server = get_env_or_raise("RESOURCE_SERVER")

        token_verifier = JWTVerifier(
            jwks_uri=f'{oauth2_domain}keys',
            issuer=oauth2_issuer,
            audience=oauth2_audience,
        )
        
        auth = RemoteAuthProvider(
            token_verifier=token_verifier,
            authorization_servers=[AnyHttpUrl(oauth2_domain)],
            resource_server_url=resource_server
        )
        return auth