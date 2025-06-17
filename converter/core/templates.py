import os

INIT_FILE = os.path.join("core", "mcp_init.py")
RUNNER_FILE = os.path.join("core", "mcp_runner.py")


def get_mcp_init_content(controller_attrs: list[str], system_prompt: str, output_dir: str) -> str:
    instances = {f"{k.replace('.', '_')} = britive_client.{k}" for k in controller_attrs}
    return f"""import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from fastmcp import FastMCP
from {output_dir}.auth.client_wrapper import BritiveClientWrapper
from fastmcp.server.auth import RemoteAuthProvider
from fastmcp.server.auth.providers.jwt import JWTVerifier
from pydantic import AnyHttpUrl
from dotenv import load_dotenv


load_dotenv()

oauth2_domain = os.environ.get("OAUTH2_DOMAIN")
oauth2_audience = os.environ.get("OAUTH2_AUDIENCE")
oauth2_issuer = os.environ.get("OAUTH2_ISSUER")
resource_server = os.environ.get("RESOURCE_SERVER")


token_verifier = JWTVerifier(
    jwks_uri=f'{{oauth2_domain}}keys',
    issuer=oauth2_issuer,
    audience=oauth2_audience,
)
 
auth = RemoteAuthProvider(
    token_verifier=token_verifier,
    authorization_servers=[AnyHttpUrl(oauth2_domain)],
    resource_server_url=resource_server
)

mcp = FastMCP(name="Britive Tool Server", auth=auth, instructions=\"\"\"{system_prompt}\"\"\")
tenant = os.getenv("BRITIVE_TENANT", "courage.dev2.aws")
if tenant is None:
    raise ValueError("BRITIVE_TENANT environment variable is required but not set")
client_wrapper = BritiveClientWrapper(tenant)
"""


def get_mcp_runner_content(output_dir: str, tools_dir: str, controller_attrs: list[str]) -> str:
    import_lines = [
        f"from {tools_dir.replace(os.sep, '.')}.{controller_attr.replace('.', '_')} import *"
        for controller_attr in controller_attrs
    ]
    joined_imports = "\n".join(import_lines)

    return f"""import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from {output_dir.replace(os.sep, ".")} import mcp
{joined_imports}

if __name__ == '__main__':
    mcp.run(transport="streamable-http", host="localhost", port=5000)
    # mcp.run()
"""
