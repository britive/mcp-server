import datetime
from britive_mcp_tools.core.mcp_init import mcp, client_wrapper
from britive.exceptions import UnauthorizedRequest
from fastmcp import Context

@mcp.tool(name="identity_management_service_identities_list", description="""Use this tool **only if the user has confirmed they are referring to service identities**. Do not assume the type of identity.This tool lists all service identities available in the Britive platform. It provides list of details such as identity ID, name, type, and status. Use this tool to get userId based on filter options and use this id in further operations like enabling or disabling a service identity. You can filter the list by name, type, status, and tags to narrow down the results.""")
def identity_management_service_identities_list(ctx: Context, filter_expression: str = None, include_tags: bool = False):
    # This tool is generated using Britive SDK v4.3.0
    """Provide an optionally filtered list of all service identities.

:param filter_expression: filter list of users based on name, status, or role. The supported operators
     are 'eq' and 'co'. Example: 'name co "Smith"'
:param include_tags: if this is set to true, tags/group memberships are returned.
:return: List of service identity records"""

    try:
        client = client_wrapper.get_client(ctx)
        return client.identity_management.service_identities.list(filter_expression, include_tags)
    except UnauthorizedRequest:
        raise UnauthorizedRequest(
            "User is not authenticated. Please ask the user to run `pybritive login` in their terminal to log in interactively. "
            "After the user finishes logging in, ask them to confirm so you can retry this tool."
        )
    

@mcp.tool(name="identity_management_service_identities_get", description="""Use this tool **only if the user has confirmed they are referring to service identities**. Do not assume the type of identity.This tool retrieves detailed information about a specific service identity by its ID. It provides comprehensive details including the identity's name, type, status, created date, modified date, last login, token expires on, token expiration in days, type of serviceIdentity type and any associated tags. Use this tool to gather specific information about a service identity before taking actions like enabling or disabling it.""")
def identity_management_service_identities_get(ctx: Context, service_identity_id: str):
    # This tool is generated using Britive SDK v4.3.0
    """Provide details of the given service_identity.

:param service_identity_id: The ID  of the service identity.
:return: Details of the specified user."""

    try:
        client = client_wrapper.get_client(ctx)
        return client.identity_management.service_identities.get(service_identity_id)
    except UnauthorizedRequest:
        raise UnauthorizedRequest(
            "User is not authenticated. Please ask the user to run `pybritive login` in their terminal to log in interactively. "
            "After the user finishes logging in, ask them to confirm so you can retry this tool."
        )
    

@mcp.tool(name="identity_management_service_identities_search", description="""Use this tool **only if the user has confirmed they are referring to service identities**. Do not assume the type of identity.This tool searches for service identities based on a query string. It allows you to find identities by name, type, or other attributes. The search results include basic details such as identity ID, name, type, and status. Use this tool to quickly locate service identities that match specific criteria without needing to list all identities.""")
def identity_management_service_identities_search(ctx: Context, search_string: str):
    # This tool is generated using Britive SDK v4.3.0
    """Search all user fields for the given `search_string` and returns
a list of matched service identities.

:param search_string:
:return: List of user records"""

    try:
        client = client_wrapper.get_client(ctx)
        return client.identity_management.service_identities.search(search_string)
    except UnauthorizedRequest:
        raise UnauthorizedRequest(
            "User is not authenticated. Please ask the user to run `pybritive login` in their terminal to log in interactively. "
            "After the user finishes logging in, ask them to confirm so you can retry this tool."
        )
    

@mcp.tool(name="identity_management_service_identities_enable", description="""Use this tool **only if the user has confirmed they are referring to service identities**. Do not assume the type of identity.Checks the status of the specified service identity. If the status is inactive, prompts the user for confirmation to enable it. If confirmed, it performs the enable action. If the identity is already active, it informs the user and suggests disabling it instead.""")
def identity_management_service_identities_enable(ctx: Context, service_identity_id: str = None, service_identity_ids: list = None):
    # This tool is generated using Britive SDK v4.3.0
    """Enable the given service identities.

You can pass in both `service_identity_id` for a single user and `service_identity_ids` to enable multiple
service identities in one call. If both `service_identity_id` and `service_identity_ids` are provided they
will be merged together into one list.

:param service_identity_id: The ID of the user you wish to enable.
:param service_identity_ids: A list of user IDs that you wish to enable.
:return: if `service_identity_ids` is set will return a list of user records, else returns a user dict"""

    try:
        client = client_wrapper.get_client(ctx)
        return client.identity_management.service_identities.enable(service_identity_id, service_identity_ids)
    except UnauthorizedRequest:
        raise UnauthorizedRequest(
            "User is not authenticated. Please ask the user to run `pybritive login` in their terminal to log in interactively. "
            "After the user finishes logging in, ask them to confirm so you can retry this tool."
        )
    

@mcp.tool(name="identity_management_service_identities_disable", description="""Use this tool **only if the user has confirmed they are referring to service identities**. Do not assume the type of identity.Checks the status of the specified service identity. If the status is active, prompts the user for confirmation to disable it. If confirmed, it performs the disable action. If the identity is already inactive, it informs the user and suggests enabling it instead.""")
def identity_management_service_identities_disable(ctx: Context, service_identity_id: str = None, service_identity_ids: list = None):
    # This tool is generated using Britive SDK v4.3.0
    """Disable the given service identities.

You can pass in both `service_identity_id` for a single service identity and `service_identity_ids` to disable
multiple service identitie at in one call. If both `service_identity_id` and `service_identity_ids` are
provided they will be merged together into one list.

:param service_identity_id: The ID of the user you wish to disable.
:param service_identity_ids: A list of user IDs that you wish to disable.
:return: if `user_ids` is set will return a list of user records, else returns a user dict"""

    try:
        client = client_wrapper.get_client(ctx)
        return client.identity_management.service_identities.disable(service_identity_id, service_identity_ids)
    except UnauthorizedRequest:
        raise UnauthorizedRequest(
            "User is not authenticated. Please ask the user to run `pybritive login` in their terminal to log in interactively. "
            "After the user finishes logging in, ask them to confirm so you can retry this tool."
        )
    
