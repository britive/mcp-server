import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from configparser import ConfigParser

from fastmcp import Context

from britive.britive import Britive

from .token_manager import TokenManager
from fastmcp import Context


class BritiveClientWrapper:
    def __init__(self, tenant):
        self.token_manager = TokenManager(tenant)
        self.tenant_dns = self.get_tenant_dns(tenant)

    def get_tenant_dns(self, tenant):
        if os.environ.get("BRITIVE_STATIC_TOKEN"):
            return tenant   
        config = ConfigParser()
        config_file = os.path.expanduser("~/.britive/pybritive.config")
        config.read(config_file)
        try:
            return config[f"tenant-{tenant}"].get("name")
        except KeyError:
            raise KeyError(
                f"User not authenticated. Please ask user to run `pybritive login` to authenticate."
            )
   

    def get_client(self):
        token = self.token_manager.get_token()
        b = Britive(tenant=self.tenant_dns, token=token)
        user_agent = b.session.headers.get("User-Agent")
        b.session.headers.update({"User-Agent": f"Britive MCP Server {user_agent}"})
        return b
