import os
from converter import client_wrapper
from converter.converter_config import TOOLS, SYSTEM_PROMPT
from converter.core.utils import (
    validate_output_dir, get_controller_instance, existing_tools, 
    get_tool_func_fullname, should_generate, generate_tool_function, 
    extract_params, remove_functions_from_content
)
from converter.core.templates import INIT_FILE, RUNNER_FILE, get_mcp_init_content, get_mcp_runner_content

TOOLS_DIRECTORY = "tools"

def generate_tools_package(generate_all: bool = False, output_dir: str = None) -> None:
    """Generate MCP tool functions from Britive SDK methods."""
    britive = client_wrapper.get_client()
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
    tools_dir = os.path.join(output_dir, TOOLS_DIRECTORY)

    os.makedirs(os.path.dirname(init_file), exist_ok=True)
    os.makedirs(os.path.dirname(runner_file), exist_ok=True)
    os.makedirs(tools_dir, exist_ok=True)

    valid_controllers = [controller for controller in controller_attrs if get_controller_instance(britive, controller)]
    with open(init_file, "w") as f:
        f.write(get_mcp_init_content(valid_controllers, SYSTEM_PROMPT, output_dir.replace("/", ".")))
    
    with open(runner_file, "w") as f:
        f.write(get_mcp_runner_content(init_file.replace(".py", ""), tools_dir, controller_attrs))


    # For each controller, write a separate file
    for controller_attr, tools in TOOLS.items():
        controller_instance = get_controller_instance(britive, controller_attr)
        if not controller_instance:
            print(f"⚠️   Controller '{controller_attr}' not found in Britive SDK.")
            continue

        controller_file_path = os.path.join(tools_dir, f"{controller_attr.replace('.', '_')}.py")
        
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

        import_statement = f"import datetime\nfrom {init_file.replace(".py", "").replace('/', '.')} import mcp, client_wrapper\nfrom britive.exceptions import UnauthorizedRequest"
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