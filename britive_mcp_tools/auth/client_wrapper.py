import os
import sys
from configparser import ConfigParser
from britive.britive import Britive
from fastmcp import Context
from pybritive import britive_cli


class BritiveClientWrapper:
    def __init__(self, tenant):
        self.tenant_dns = self.get_tenant_dns(tenant)
        self.tenant = tenant
        if os.environ.get("BRITIVE_EMAIL"):
            self.obo = True
            self.email = os.environ.get("BRITIVE_EMAIL")
        else:
            self.obo = False
            self.email = None

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

    def get_token(self):
        if os.environ.get("BRITIVE_STATIC_TOKEN"):
            return os.environ.get("BRITIVE_STATIC_TOKEN")
        temp_cli = britive_cli.BritiveCli(tenant_name=self.tenant)
        temp_cli.login()
        temp_cli.set_credential_manager()
        return temp_cli.credential_manager.credentials["accessToken"]

    def get_client(self):
        token = self.get_token()
        b = Britive(tenant=self.tenant_dns, token=token)
        user_agent = b.session.headers.get("User-Agent")
        b.session.headers.update({"User-Agent": f"Britive MCP Server {user_agent}"})
        return b
