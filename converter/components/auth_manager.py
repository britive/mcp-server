import os
from components.utils import get_env_or_raise
from components.oauth_provider import OAuthProvider
from components.pybritive_login_provider import PyBritiveLoginProvider
from components.static_token_provider import StaticTokenProvider


class AuthManager:
    """
    Determines which authentication provider to use.
    
    Priority:
        1. Static Token (BRITIVE_STATIC_TOKEN)
        2. OAuth (OAUTH2_DOMAIN)
        3. PyBritive Login (default fallback)
    
    You can also explicitly select the provider by passing:
        - "static"  -> StaticTokenProvider
        - "oauth"   -> OAuthProvider
        - "pybritive" -> PyBritiveLoginProvider
    """

    PROVIDER_MAP = {
        "static": StaticTokenProvider,
        "oauth": OAuthProvider,
        "pybritive": PyBritiveLoginProvider,
    }

    def __init__(self, auth_provider: str = None):
        """
        :param provider: Optional string specifying the provider: "static", "oauth", or "pybritive"
        """
        self.tenant = get_env_or_raise("BRITIVE_TENANT")
        self.auth_provider = self._get_auth_provider(auth_provider)

    def _get_auth_provider(self, auth_provider: str = None):
        """
        Select the AuthProvider based on user input or environment variables.
        Priority:
          1. User-specified provider
          2. Environment-based fallback
          3. Default fallback to PyBritiveLoginProvider
        """

        if auth_provider:
            auth_provider = auth_provider.lower()
            if auth_provider not in self.PROVIDER_MAP:
                raise ValueError(
                    f"Invalid auth provider '{auth_provider}'. "
                    f"Choose one of: {list(self.PROVIDER_MAP.keys())}"
                )
            return self.PROVIDER_MAP[auth_provider](self.tenant)

        if os.getenv("BRITIVE_STATIC_TOKEN"):
            return StaticTokenProvider(self.tenant)
        if os.getenv("OAUTH2_DOMAIN"):
            return OAuthProvider(self.tenant)

        return PyBritiveLoginProvider(self.tenant)

    def get_provider(self):
        """Return the chosen AuthProvider instance."""
        return self.auth_provider
