import datetime
from britive_mcp_tools.core.mcp_init import mcp, client_wrapper
from britive.exceptions import UnauthorizedRequest
from fastmcp import Context

@mcp.tool(name="application_management_applications_list", description="""Use this tool to retrieve a list of all applications available in the Britive tenant. This is typically the first step when identifying applications by name or filtering them based on user input. The results can be used to extract application IDs required for other tools.""")
def application_management_applications_list(ctx: Context, extended: bool = True):
    # This tool is generated using Britive SDK v4.3.0
    """Return a list of applications in the Britive tenant.

:param extended: if True, will return additional details of the applications
:return: List of applications."""

    try:
        client = client_wrapper.get_client(ctx)
        return client.application_management.applications.list(extended)
    except UnauthorizedRequest:
        raise UnauthorizedRequest(
            "User is not authenticated. Please ask the user to run `pybritive login` in their terminal to log in interactively. "
            "After the user finishes logging in, ask them to confirm so you can retry this tool."
        )
    

@mcp.tool(name="application_management_applications_get", description="""Use this tool to fetch detailed information about a specific application using its application ID. This includes metadata such as the application's nativeId, which is essential for querying permissions or identity associations in other tools.""")
def application_management_applications_get(ctx: Context, application_id: str):
    # This tool is generated using Britive SDK v4.3.0
    """Return details of the specified application

:param application_id: The ID of the application.
:return: Details of the application."""

    try:
        client = client_wrapper.get_client(ctx)
        return client.application_management.applications.get(application_id)
    except UnauthorizedRequest:
        raise UnauthorizedRequest(
            "User is not authenticated. Please ask the user to run `pybritive login` in their terminal to log in interactively. "
            "After the user finishes logging in, ask them to confirm so you can retry this tool."
        )
    
