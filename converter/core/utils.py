import os, shutil, re, inspect, logging
from typing import Callable, List, Any, Optional
from britive import __version__ as britive_version
from britive.britive import Britive
from converter.core.logger import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

def validate_output_dir(generate_all: bool, output_dir: str) -> None:
    if not output_dir:
        raise ValueError("Output directory must be specified when generating tools.")
    if generate_all:
        if os.path.exists(output_dir):
            logger.warning(f"⚠️   Output directory '{output_dir}' already exists. Do you want to overwrite it? (y/n)")
            response = input().strip().lower()
            if response != 'y':
                raise FileExistsError(f"Output directory '{output_dir}' already exists. Please choose a different directory or remove it.")
            else:                
                shutil.rmtree(output_dir)
        try:
            os.makedirs(output_dir)
        except FileExistsError:
            raise FileExistsError(f"Output directory '{output_dir}' already exists. Please choose a different directory or remove it.")
    elif not generate_all and not os.path.exists(output_dir):
        raise FileNotFoundError(f"Output directory '{output_dir}' does not exist. Please create it by using --all to generate all tools.")
    
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

def should_generate(tool, func_name, existing_funcs):
    # Generate if not present, or present and 'regenerate' is True
    if func_name not in existing_funcs:
        return True
    return tool.regenerate

def process_method_docstring(method: Callable) -> str:
    docstring = inspect.getdoc(method)
    return f'    """{docstring}"""' if docstring else ""

def generate_tool_function(func_name: str, method: Callable, attr: str, description: Optional[str], params: List[inspect.Parameter], args: List[str]) -> str:
    decorator = f'@mcp.tool(name="{func_name}"' + (f', description="""{description}"""' if description else "") + ")"
    param_str = ", ".join(str(p) for p in params)
    args_str = ", ".join(args)
    controller_instance = attr.replace('.', '_')
    body = f"""
    try:
        client = client_wrapper.get_client(ctx)
        return client.{attr}.{method.__name__}({args_str})
    except UnauthorizedRequest:
        raise UnauthorizedRequest(
            "User is not authenticated. Please ask the user to run `pybritive login` in their terminal to log in interactively. "
            "After the user finishes logging in, ask them to confirm so you can retry this tool."
        )
    """
    docstring = process_method_docstring(method)
    tool_version = f"    # This tool is generated using Britive SDK v{britive_version}"
    return "\n".join([decorator, f"def {func_name}(ctx: Context, {param_str}):", tool_version, docstring, body])


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
        # This is just a temporary fix for list type bug in Britive SDK
        if inspect.isfunction(param.annotation):
            param = param.replace(annotation=list)
        if is_supported_parameter_type(param.annotation if param.annotation != inspect.Parameter.empty else None):
            valid_params.append(param)
            call_args.append(param.name)
        else:
            call_args.append("None")
    return valid_params, call_args

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