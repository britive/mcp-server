import datetime
from britive_mcp_tools.core.mcp_init import mcp, auth_manager
from britive.exceptions import UnauthorizedRequest
from fastmcp import Context

@mcp.tool(name="identity_management_tags_list", description="""Use this tool **only if the user has confirmed they are referring to tags identities**. Do not assume the type of identity.This tool lists all tag identities available in the Britive platform. It provides list of details such as tagId, name, type, and status. Use this tool to get tagId based on filter options and use this id in further operations like enabling or disabling a tag identity. You can filter the list by name, type, status, and tags to narrow down the results.""")
def identity_management_tags_list(ctx: Context, filter_expression: str = None):
    # This tool is generated using Britive SDK v4.3.0
    """List all tags, optionally filtered via name or status.

:param filter_expression: Filter the list of tags based on name or status. The supported operators are
    `eq' and `co`. An example is `status eq 'Active'`
:return: List of tags."""

    try:
        client = auth_manager.auth_provider.get_client(ctx)
        return client.identity_management.tags.list(filter_expression)
    except UnauthorizedRequest:
        raise UnauthorizedRequest(
            "User is not authenticated. Please ask the user to run `pybritive login` in their terminal to log in interactively. "
            "After the user finishes logging in, ask them to confirm so you can retry this tool."
        )
    

@mcp.tool(name="identity_management_tags_get", description="""Use this tool **only if the user has confirmed they are referring to tags identities**. Do not assume the type of identity.This tool retrieves detailed information about a specific tag identity by its tagID. It provides comprehensive details including the identity's name, type, status, created date, modified date, last login, token expires on, token expiration in days, type of serviceIdentity type and any associated tags. Use this tool to gather specific information about a service identity before taking actions like enabling or disabling it """)
def identity_management_tags_get(ctx: Context, tag_id: str):
    # This tool is generated using Britive SDK v4.3.0
    """Return details of a tag.

:param tag_id: The ID of the tag.
:return: Details of the tag."""

    try:
        client = auth_manager.auth_provider.get_client(ctx)
        return client.identity_management.tags.get(tag_id)
    except UnauthorizedRequest:
        raise UnauthorizedRequest(
            "User is not authenticated. Please ask the user to run `pybritive login` in their terminal to log in interactively. "
            "After the user finishes logging in, ask them to confirm so you can retry this tool."
        )
    

@mcp.tool(name="identity_management_tags_search", description="""Use this tool **only if the user has confirmed they are referring to tags identities**. Do not assume the type of identity.This tool searches for tag identities based on a query string. It allows you to find identities by name, type, or other attributes. The search results include basic details such as identity ID, name, type, and status. Use this tool to quickly locate tag identities that match specific criteria without needing to list all identities.""")
def identity_management_tags_search(ctx: Context, search_string: str):
    # This tool is generated using Britive SDK v4.3.0
    """Searche all tag fields for the given `search_string` and returns
a list of matched tags.

:param search_string: String to search.
:return: List of user records."""

    try:
        client = auth_manager.auth_provider.get_client(ctx)
        return client.identity_management.tags.search(search_string)
    except UnauthorizedRequest:
        raise UnauthorizedRequest(
            "User is not authenticated. Please ask the user to run `pybritive login` in their terminal to log in interactively. "
            "After the user finishes logging in, ask them to confirm so you can retry this tool."
        )
    

@mcp.tool(name="identity_management_tags_enable", description="""Use this tool **only if the user has confirmed they are referring to tags identities**. Do not assume the type of identity.Checks the status of the specified tag identity. If the status is inactive, prompts the user for confirmation to enable it. If confirmed, it performs the enable action. If the identity is already active, it informs the user and suggests disabling it instead.""")
def identity_management_tags_enable(ctx: Context, tag_id: str):
    # This tool is generated using Britive SDK v4.3.0
    """Enable a tag.

:param tag_id: The ID of the tag.
:return: Details of the tag."""

    try:
        client = auth_manager.auth_provider.get_client(ctx)
        return client.identity_management.tags.enable(tag_id)
    except UnauthorizedRequest:
        raise UnauthorizedRequest(
            "User is not authenticated. Please ask the user to run `pybritive login` in their terminal to log in interactively. "
            "After the user finishes logging in, ask them to confirm so you can retry this tool."
        )
    

@mcp.tool(name="identity_management_tags_disable", description="""Use this tool **only if the user has confirmed they are referring to tags identities**. Do not assume the type of identity.Checks the status of the specified tag identity. If the status is active, prompts the user for confirmation to disable it. If confirmed, it performs the disable action. If the identity is already inactive, it informs the user and suggests enabling it instead.""")
def identity_management_tags_disable(ctx: Context, tag_id: str):
    # This tool is generated using Britive SDK v4.3.0
    """Disable a tag.

:param tag_id: The ID of the tag.
:return: Details of the tag."""

    try:
        client = auth_manager.auth_provider.get_client(ctx)
        return client.identity_management.tags.disable(tag_id)
    except UnauthorizedRequest:
        raise UnauthorizedRequest(
            "User is not authenticated. Please ask the user to run `pybritive login` in their terminal to log in interactively. "
            "After the user finishes logging in, ask them to confirm so you can retry this tool."
        )
    
