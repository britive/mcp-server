import os
import re
import inspect
from britive import __version__ as britive_version
from britive.britive import Britive
from britive.exceptions import UnauthorizedRequest
from converter_config import SYSTEM_PROMPT, TOOLS
from dotenv import load_dotenv
from typing import Callable, List, Any, Optional
from configparser import ConfigParser

load_dotenv()

INIT_FILE = "__init__.py"
RUNNER_FILE = "runner.py"

def get_init_file_content(controller_attrs: List[str]) -> str:
    instances = {
        f"{k.replace('.', '_')} = britive.{k}" for k in controller_attrs
    }
    return f"""import os
from configparser import ConfigParser
from fastmcp import FastMCP
from britive.britive import Britive
from dotenv import load_dotenv
from britive.exceptions import UnauthorizedRequest
import datetime
from typing import Optional

load_dotenv()


def britive_client(tenant: str = "") -> Britive | None:
    tenant = tenant if tenant else os.getenv("BRITIVE_TENANT", "courage.dev2.aws")
    tenant_config = ConfigParser()
    tenant_config.read(os.path.expanduser("~/.britive/pybritive.config"))
    tenant_dns = tenant_config[f"tenant-{{tenant}}"]["name"]
    token_config = ConfigParser()
    token_config.read(os.path.expanduser("~/.britive/pybritive.credentials"))
    token = token_config[tenant]["accessToken"]
    try:
        return Britive(tenant=tenant_dns, token=token)
    except UnauthorizedRequest as uae:
        print(str(uae).rsplit("-", maxsplit=1)[-1].strip()) 

mcp = FastMCP(name="Britive Tool Server", instruction=\"\"\"{SYSTEM_PROMPT}\"\"\")
britive = britive_client()

{chr(10).join(sorted(instances))}

"""

def get_britive_client(tenant: str = "") -> Britive | None:
    tenant = tenant if tenant else os.getenv("BRITIVE_TENANT", "courage.dev2.aws")
    tenant_config = ConfigParser()
    tenant_config.read(os.path.expanduser("~/.britive/pybritive.config"))
    try:
        tenant_dns = tenant_config[f"tenant-{tenant}"]["name"]
    except KeyError:
        raise KeyError("Invalid or missing Britive tenant. Please verify and enter the correct tenant name.")
    token_config = ConfigParser()
    token_config.read(os.path.expanduser("~/.britive/pybritive.credentials"))
    try:
        token = token_config[tenant]["accessToken"]
    except KeyError:
        raise KeyError("Authentication required: No access token detected. Run 'pybritive login' to authenticate before using the converter.")
    try:
        return Britive(tenant=tenant_dns, token=token)
    except UnauthorizedRequest:
        raise UnauthorizedRequest("Authentication required: No access token detected. Run 'pybritive login' to authenticate before using the converter.")

def get_runner_file_content(output_dir: str, controller_attrs: list[str]) -> str:
    import_lines = [f"from {output_dir.replace('/', '.')}.{controller_attr.replace('.', '_')} import *" for controller_attr in controller_attrs]
    joined_imports = "\n".join(import_lines)

    return f"""from {output_dir.replace('/', '.')} import mcp
{joined_imports}

if __name__ == '__main__':
    mcp.run()
"""



def is_supported_parameter_type(param_type: Any) -> bool:
    unsupported = {Callable, object}
    origin = getattr(param_type, "__origin__", None)
    name = str(getattr(param_type, "_name", ""))
    return param_type not in unsupported and origin not in unsupported and not any(
        u.__name__ in str(param_type) or u.__name__ in name for u in unsupported)


def extract_params(method: Callable) -> tuple[List[inspect.Parameter], List[str]]:
    sig = inspect.signature(method)
    valid_params, call_args = [], []
    for param in sig.parameters.values():
        if is_supported_parameter_type(param.annotation if param.annotation != inspect.Parameter.empty else None):
            valid_params.append(param)
            call_args.append(param.name)
        else:
            call_args.append("None")
    return valid_params, call_args


def get_controller_instance(britive: Britive, controller_attr: str) -> Optional[object]:
    try:
        for part in controller_attr.split("."):
            britive = getattr(britive, part)
        return britive
    except AttributeError:
        return None
    
def existing_tools(filepath: str) -> set:
    if not os.path.exists(filepath):
        return set()
    with open(filepath, "r") as f:
        return set(re.findall(r'@mcp\.tool\(name=["\']([a-zA-Z0-9_]+)["\']', f.read()))
    
def get_tool_func_fullname(controller_attr, tool):
    return tool.tool_name or f"{controller_attr.replace('.', '_')}_{tool.function_name}"


def process_method_docstring(method: Callable) -> str:
    docstring = inspect.getdoc(method)
    return f'    """{docstring}"""' if docstring else ""

def validate_output_dir(generate_all: bool, output_dir: str) -> None:
    if not output_dir:
        raise ValueError("Output directory must be specified when generating tools.")
    if generate_all:
        try:
            os.makedirs(output_dir)
        except FileExistsError:
            raise FileExistsError(f"Output directory '{output_dir}' already exists. Please choose a different directory or remove it.")
    elif not generate_all and not os.path.exists(output_dir):
        raise FileNotFoundError(f"Output directory '{output_dir}' does not exist. Please create it by using --all to generate all tools.")
    
def should_generate(tool, func_name, existing_funcs):
    # Generate if not present, or present and 'regenerate' is True
    if func_name not in existing_funcs:
        return True
    return tool.regenerate

def generate_tool_function(func_name: str, method: Callable, attr: str, description: Optional[str], params: List[inspect.Parameter], args: List[str]) -> str:
    decorator = f'@mcp.tool(name="{func_name}"' + (f', description="""{description}"""' if description else "") + ")"
    param_str = ", ".join(str(p) for p in params)
    args_str = ", ".join(args)
    controller_instance = attr.replace('.', '_')
    body = f"    return {controller_instance}.{method.__name__}({args_str})"
    docstring = process_method_docstring(method)
    tool_version = f"    # This tool is generated using Britive SDK v{britive_version}"
    return "\n".join([decorator, f"def {func_name}({param_str}):", tool_version, docstring, body])

def remove_functions_from_content(content: str, func_names: set) -> str:
    """Remove all tool functions (decorator + def block) with names in func_names from the content."""
    for func_name in func_names:
        content = re.sub(
            rf'\n*@mcp\.tool\(name=["\']{func_name}["\'].*?\)\n'
            rf'def {func_name}\(.*?\):.*?(?=(\n@|\nif __name__ == [\'"]__main__[\'"]|$))',
            '',
            content,
            flags=re.DOTALL
        )
    return content

def generate_tools_package(generate_all: bool = False, output_dir: str = None) -> None:
    """Generate MCP tool functions from Britive SDK methods."""
    britive = get_britive_client()
    existing_tool_names = set()
    new_tool_funcs = []
    new_tool_names = []
    funcs_to_remove = set()
    content_to_write = ""
    new_tools_count = 0

    # Validate output directory
    validate_output_dir(generate_all, output_dir)
        
    # Write __init__.py with all initializations
    controller_attrs = list(TOOLS.keys())
    init_file = os.path.join(output_dir, INIT_FILE)
    runner_file = os.path.join(output_dir, RUNNER_FILE)


    valid_controllers = [controller for controller in controller_attrs if get_controller_instance(britive, controller)]
    with open(init_file, "w") as f:
        f.write(get_init_file_content(valid_controllers))
    
    with open(runner_file, "w") as f:
        f.write(get_runner_file_content(output_dir, controller_attrs))


    # For each controller, write a separate file
    for controller_attr, tools in TOOLS.items():
        controller_instance = get_controller_instance(britive, controller_attr)
        if not controller_instance:
            print(f"⚠️   Controller '{controller_attr}' not found in Britive SDK.")
            continue

        controller_file_path = os.path.join(output_dir, f"{controller_attr.replace('.', '_')}.py")
        
        existing_tool_names = existing_tools(controller_file_path) if not generate_all else set()

        for tool in tools:
            sdk_func_name = tool.function_name
            tool_func_name = get_tool_func_fullname(controller_attr, tool)
            ai_description = tool.ai_description
            
            if not generate_all and not should_generate(tool, tool_func_name, existing_tool_names):
                continue
            
            method = getattr(controller_instance, sdk_func_name, None)
            if not method or sdk_func_name.startswith('_'):
                if not method:
                    print(f"⚠️   Method '{sdk_func_name}' not found in controller '{controller_attr}'.")
                continue
            
            filtered_params, call_args = extract_params(method)
            new_tool_funcs.append(generate_tool_function(
                tool_func_name, method, controller_attr, ai_description, filtered_params, call_args
            ))
            new_tool_names.append(tool_func_name)

            if not generate_all and tool_func_name in existing_tool_names:
                funcs_to_remove.add(tool_func_name)

        import_statement = f"import datetime\nfrom {output_dir.replace('/', '.')} import mcp, {controller_attr.replace('.', '_')}"
        if generate_all:
            # Write the new tool functions to the controller file
            with open(controller_file_path, "w") as f:
                f.write(import_statement + "\n\n")
                f.write("\n\n".join(new_tool_funcs))
                f.write("\n")
            new_tools_count += len(new_tool_funcs)
            tool_list = '\n   • '.join(new_tool_names)
            print(f"[✅] Generated '{controller_file_path}' with {len(new_tool_funcs)} tool(s)\n   • {tool_list}")
        else:
            content_to_write = open(controller_file_path).read() if os.path.exists(controller_file_path) else ""
            if funcs_to_remove:
                content_to_write = remove_functions_from_content(
                    content_to_write, funcs_to_remove
                )
            
            if new_tool_funcs:
                add_file_header = not os.path.exists(controller_file_path)
                with open(controller_file_path, "w") as f:
                    f.write(f"{import_statement}\n\n" if add_file_header else "")
                    joined_funcs = "\n\n".join(new_tool_funcs)
                    f.write(f"{content_to_write}\n\n{joined_funcs}")
                    f.write("\n")
                new_tools_count += len(new_tool_funcs)
                tool_list = '\n   • '.join(new_tool_names)
                print(f"[✅] Updated '{controller_file_path}' with {len(new_tool_funcs)} tool(s): \n   • {tool_list}")
        new_tool_funcs.clear()
        new_tool_names.clear()

    if new_tools_count:
        print(f"\n[✅] Total new tools generated: {new_tools_count}")
    else:
        print("[ℹ️] No new tools generated. Ensure to add new tools in the config.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()

    # Output directory for the generating tools
    parser.add_argument('--output', type=str, help='Output folder name to generate the tools package')

    # Flag to generate all tools
    parser.add_argument('--all', action='store_true', help='Generate all tools from Britive SDK')

    args = parser.parse_args()
    generate_tools_package(args.all, args.output.replace("\\", "/"))