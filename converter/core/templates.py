import os

INIT_FILE = os.path.join("core", "mcp_init.py")
RUNNER_FILE = os.path.join("core", "mcp_runner.py")

CONVERTER_AUTH_MANAGER = os.path.join("converter", "components", "auth_manager.py")
CONVERTER_OAUTH_PROVIDER = os.path.join("converter", "components", "oauth_provider.py")
CONVERTER_PYBRITIVE_LOGIN_PROVIDER = os.path.join("converter", "components", "pybritive_login_provider.py")
CONVERTER_STATIC_TOKEN_PROVIDER = os.path.join("converter", "components", "static_token_provider.py")

AUTH_MANAGER = os.path.join("auth", "auth_manager.py")
OAUTH_PROVIDER = os.path.join("auth", "oauth_provider.py")
PYBRITIVE_LOGIN_PROVIDER = os.path.join("auth", "pybritive_login_provider.py")
STATIC_TOKEN_PROVIDER = os.path.join("auth", "static_token_provider.py")

def get_mcp_init_content(controller_attrs: list[str], system_prompt: str, output_dir: str) -> str:
    instances = {f"{k.replace('.', '_')} = britive_client.{k}" for k in controller_attrs}
    return f"""import os
import sys
from fastmcp import FastMCP
from dotenv import load_dotenv

from {output_dir}.auth.auth_manager import AuthManager

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
load_dotenv()


auth_manager = AuthManager()
auth = auth_manager.auth_provider.get_auth()

mcp = FastMCP(name="Britive Tool Server", auth=auth, instructions=\"\"\"{system_prompt}\"\"\")

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
    mcp.run()
"""

def get_auth_manager_content(output_dir: str) -> str:

    replacements = {
        "from components.utils": f"from {output_dir}.utils",
        "from components.oauth_provider": f"from {output_dir}.auth.oauth_provider",
        "from components.pybritive_login_provider": f"from {output_dir}.auth.pybritive_login_provider",
        "from components.static_token_provider": f"from {output_dir}.auth.static_token_provider"
    }

    # Read file content
    with open(CONVERTER_AUTH_MANAGER, "r", encoding="utf-8") as file:
        content = file.read()

    # Replace imports
    for old_import, new_import in replacements.items():
        content = content.replace(old_import, new_import)

    return content
    
def get_oauth_provider_content(output_dir: str) -> str:

    replacements = {
        "from components.auth_provider": f"from {output_dir}.auth.auth_provider",
        "from components.utils": f"from {output_dir}.utils",
    }

    # Read file content
    with open(os.path.join("converter", "components", "oauth_provider.py"), "r", encoding="utf-8") as file:
        content = file.read()

    # Replace imports
    for old_import, new_import in replacements.items():
        content = content.replace(old_import, new_import)
    
    return content

def get_pybritive_login_provider_content(output_dir: str) -> str:

    replacements = {
        "from components.auth_provider": f"from {output_dir}.auth.auth_provider",
    }

    # Read file content
    with open(os.path.join("converter", "components", "pybritive_login_provider.py"), "r", encoding="utf-8") as file:
        content = file.read()

    # Replace imports
    for old_import, new_import in replacements.items():
        content = content.replace(old_import, new_import)

    return content

def get_static_token_provider_content(output_dir: str) -> str:
    
    replacements = {
        "from components.auth_provider": f"from {output_dir}.auth.auth_provider",
    }

    # Read file content
    with open(os.path.join("converter", "components", "static_token_provider.py"), "r", encoding="utf-8") as file:
        content = file.read()

    # Replace imports
    for old_import, new_import in replacements.items():
        content = content.replace(old_import, new_import)

    return content