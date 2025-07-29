import os

INIT_FILE = os.path.join("core", "mcp_init.py")
RUNNER_FILE = os.path.join("core", "mcp_runner.py")

def get_mcp_init_content(controller_attrs: list[str], system_prompt: str, output_dir: str) -> str:
    instances = {
        f"{k.replace('.', '_')} = britive_client.{k}" for k in controller_attrs
    }
    return f"""import os
from fastmcp import FastMCP
from {output_dir}.auth.client_wrapper import BritiveClientWrapper

mcp = FastMCP(name="Britive Tool Server", instructions=\"\"\"{system_prompt}\"\"\")
tenant = os.getenv("BRITIVE_TENANT")
if tenant is None:
    raise ValueError("BRITIVE_TENANT environment variable is required but not set")
client_wrapper = BritiveClientWrapper(tenant)
"""

def get_mcp_runner_content(output_dir: str, tools_dir: str, controller_attrs: list[str]) -> str:
    import_lines = [f"from {tools_dir.replace(os.sep, '.')}.{controller_attr.replace('.', '_')} import *" for controller_attr in controller_attrs]
    joined_imports = "\n".join(import_lines)

    return f"""from {output_dir.replace(os.sep, '.')} import mcp
{joined_imports}

if __name__ == '__main__':
    mcp.run()
"""
