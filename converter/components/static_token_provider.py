import os
from components.auth_provider import AuthProvider
from britive.britive import Britive


class StaticTokenProvider(AuthProvider):
    """
    Auth provider using a static token from an environment variable
    and tenant DNS passed by the user.
    """

    def __init__(self, tenant: str):
        self.tenant = tenant
        self.token = os.environ.get("BRITIVE_STATIC_TOKEN")

    def _get_token(self) -> str:
        return self.token

    def _get_tenant_dns(self) -> str:
        return self.tenant

    def get_client(self, ctx) -> Britive:
        """
        Returns an authenticated Britive client instance.
        """
        token = self._get_token()
        tenant_dns = self._get_tenant_dns()
        client = Britive(tenant=tenant_dns, token=token)

        # Update User-Agent for MCP integration
        user_agent = client.session.headers.get("User-Agent", "")
        client.session.headers.update({"User-Agent": f"Britive MCP Server {user_agent}"})
        return client

    def get_auth(self) -> None:
        return None