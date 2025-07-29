import os
import time
from configparser import ConfigParser

class TokenManager:
    def __init__(self, tenant="courage.dev2.aws"):
        self.tenant = tenant
        self.token_file = os.path.expanduser("~/.britive/pybritive.credentials")
        self.config = ConfigParser()

    def get_token(self):
        static_token = os.getenv("BRITIVE_STATIC_TOKEN")
        if static_token:
            return static_token
        else:
            self.config.read(self.token_file)
            try:
                return self.get_valid_token()
            except KeyError:
                self.config = ConfigParser()
                raise KeyError(f"User not authenticated. Please ask user to run `pybritive login` to authenticate.")
            

    def get_valid_token(self):
        token_error = "User not authenticated. Please ask user to run `pybritive login` to authenticate."
        try:
            token = self.config[self.tenant].get("accessToken")
            token_expiry = int(self.config[self.tenant].get("safeExpirationTime", "0"))
            if not token or time.time() > token_expiry:
                raise KeyError(token_error)
            self.config = ConfigParser()
            return token
        except KeyError:
            self.config = ConfigParser()
            raise KeyError(token_error)
