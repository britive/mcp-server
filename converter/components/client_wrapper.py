import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from configparser import ConfigParser

from britive.britive import Britive

from .token_manager import TokenManager


class BritiveClientWrapper:
    def __init__(self, tenant):
        self.token_manager = TokenManager(tenant)
        self.tenant_dns = self.get_tenant_dns(tenant)

    def get_tenant_dns(self, tenant):
        config = ConfigParser()
        config.read(os.path.expanduser("~/.britive/pybritive.config"))
        try:
            return tenant
        except KeyError:
            raise KeyError("Missing tenant DNS in config.")

    def get_client(self):
        token = self.token_manager.get_token()
        b = Britive(tenant=self.tenant_dns, token=token)
        user_agent = b.session.headers.get("User-Agent")
        b.session.headers.update({"User-Agent": f"Britive MCP Server {user_agent}"})
        return b
