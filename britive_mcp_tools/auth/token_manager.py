import os
import time
import sys
import subprocess
from configparser import ConfigParser

class TokenManager:
    def __init__(self, tenant="courage.dev2.aws"):
        self.tenant = tenant
        self.token_file = os.path.expanduser("~/.britive/pybritive.credentials")
        self.config = ConfigParser()
        self.token_expiry_buffer = 60
        self.read_token()

    def read_token(self):
        if os.getenv("BRITIVE_STATIC_TOKEN"):
            self.token = os.getenv("BRITIVE_STATIC_TOKEN")
        else:
            self.config.read(self.token_file)
            try:
                self.token = self.config[self.tenant]["accessToken"]
                self.expiry = int(self.config[self.tenant].get("safeExpirationTime", "0"))
            except KeyError:
                self.token = None
                self.expiry = 0

    def is_expired(self):
        return not self.token or (time.time() + self.token_expiry_buffer) > self.expiry

    def is_logged_out(self):
        self.config.read(self.token_file)
        return self.tenant not in self.config
    
    def refresh_token(self):
        pybritive_cli = os.path.join(os.path.dirname(sys.executable), "pybritive")
        subprocess.run([pybritive_cli, "login"], check=True)
        self.read_token()

    def get_token(self):
        britive_static_token = os.getenv("BRITIVE_STATIC_TOKEN")
        if britive_static_token:
            self.token = britive_static_token
            return self.token
        if self.is_expired() or self.is_logged_out():
            self.refresh_token()
        return self.token
