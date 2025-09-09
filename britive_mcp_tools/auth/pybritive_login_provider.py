import os
import time
from configparser import ConfigParser

from pybritive.helpers.encryption import StringEncryption
from britive_mcp_tools.auth.auth_provider import AuthProvider
from britive.britive import Britive


class AuthenticationError(Exception):
    """Custom exception for authentication-related errors."""
    pass


class TenantConfigurationError(Exception):
    """Custom exception for tenant configuration-related errors."""
    pass


class PyBritiveLoginProvider(AuthProvider):
    """
    Handles authentication with Britive using encrypted credentials stored locally.
    """

    TOKEN_FILE = os.path.expanduser("~/.britive/pybritive.credentials.encrypted")
    CONFIG_FILE = os.path.expanduser("~/.britive/pybritive.config")

    def __init__(self, tenant: str):
        self.tenant = tenant
        self.encryption = StringEncryption()

    def _load_token_config(self) -> ConfigParser:
        config = ConfigParser()
        config.read(self.TOKEN_FILE)
        return config

    def _load_main_config(self) -> ConfigParser:
        config = ConfigParser()
        config.read(self.CONFIG_FILE)
        return config

    def _get_token(self) -> str:
        """
        Retrieves and validates the decrypted token for the current tenant.
        Raises AuthenticationError if invalid or expired.
        """
        config = self._load_token_config()
        if self.tenant not in config:
            raise AuthenticationError("User not authenticated. Please run `pybritive login`.")

        try:
            encrypted_token = config[self.tenant].get("accessToken")
            token = self.encryption.decrypt(encrypted_token)
            expiry = int(config[self.tenant].get("safeExpirationTime", "0"))

            if not token or time.time() > expiry:
                raise AuthenticationError("Token expired or invalid. Please run `pybritive login`.")
            return token
        except KeyError:
            raise AuthenticationError("Authentication details missing. Please run `pybritive login`.")

    def _get_tenant_dns(self) -> str:
        """
        Retrieves the DNS for the tenant from configuration.
        Raises TenantConfigurationError if missing.
        """
        config = self._load_main_config()
        section = f"tenant-{self.tenant}"
        if section not in config:
            raise TenantConfigurationError(
                "Missing tenant DNS in config. Configure using `pybritive configure tenant`."
            )
        return config[section].get("name")

    def get_client(self, ctx) -> Britive:
        """
        Returns an authenticated Britive client instance.
        Always reloads configs from disk for each call.
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