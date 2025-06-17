import datetime

from britive.exceptions import UnauthorizedRequest
from fastmcp import Context

from britive_mcp_tools.core.mcp_init import client_wrapper, mcp


@mcp.tool(
    name="identity_management_users_list",
    description="""Use this tool **only if the user has confirmed they are referring to user identities**. Do not assume the type of identity.This tool lists all user identities available in the Britive platform with optional filters. It provides list of details such as userID, username, type, status, email, firstName, lastName. Use this tool to get userId based on filter options and use this id in further operations like enabling or disabling a service identity. You can filter the list by username, type, status, and tags to narrow down the results.""",
)
def identity_management_users_list(
    filter_expression: str = None, include_tags: bool = False
):
    # This tool is generated using Britive SDK v4.3.0
    """Provide an optionally filtered list of all users.

    :param filter_expression: filter list of users based on name, status, or role. The supported operators
         are 'eq' and 'co'. Example: 'name co "Smith"'
    :param include_tags: if this is set to true, tags/group memberships are returned.
    :return: List of user records"""

    try:
        client = client_wrapper.get_client()
        return client.identity_management.users.list(filter_expression, include_tags)
    except UnauthorizedRequest:
        raise UnauthorizedRequest(
            "User is not authenticated. Please ask the user to run `pybritive login` in their terminal to log in interactively. "
            "After the user finishes logging in, ask them to confirm so you can retry this tool."
        )


@mcp.tool(
    name="identity_management_users_get",
    description="""Use this tool **only if the user has confirmed they are referring to user identities**. Do not assume the type of identity.This tool retrieves detailed information about a specific user identity by its userID. It provides comprehensive details including the identity's userId, username, email, firstName, lastName, type, status, created, modified, identityProvider and userTags. Use this tool to gather specific information about a user identity before taking actions like enabling or disabling it """,
)
def identity_management_users_get(user_id: str):
    # This tool is generated using Britive SDK v4.3.0
    """Provide details of the given user.

    :param user_id: The ID  of the user.
    :return: Details of the specified user."""

    try:
        client = client_wrapper.get_client()
        return client.identity_management.users.get(user_id)
    except UnauthorizedRequest:
        raise UnauthorizedRequest(
            "User is not authenticated. Please ask the user to run `pybritive login` in their terminal to log in interactively. "
            "After the user finishes logging in, ask them to confirm so you can retry this tool."
        )


@mcp.tool(
    name="identity_management_users_search",
    description="""Use this tool **only if the user has confirmed they are referring to user identities**. Do not assume the type of identity.This tool searches for user identities based on a query string. It allows you to find identities by name, username, firstName, lastName, email, type, status, identityProvider or other attributes. The search results include basic details such as userId, name, type, and status. Use this tool to quickly locate user identities that match specific criteria without needing to list all identities.""",
)
def identity_management_users_search(search_string: str):
    # This tool is generated using Britive SDK v4.3.0
    """Search all user fields for the given `search_string`.

    :param search_string: String to search.
    :return: List of user records."""

    try:
        client = client_wrapper.get_client()
        return client.identity_management.users.search(search_string)
    except UnauthorizedRequest:
        raise UnauthorizedRequest(
            "User is not authenticated. Please ask the user to run `pybritive login` in their terminal to log in interactively. "
            "After the user finishes logging in, ask them to confirm so you can retry this tool."
        )


@mcp.tool(
    name="identity_management_users_enable",
    description="""Use this tool **only if the user has confirmed they are referring to user identities**. Do not assume the type of identity.Checks the status of the specified user identity. If the status is inactive, prompts the user for confirmation to enable it. If confirmed, it performs the enable action. If the identity is already active, it informs the user and suggests disabling it instead.""",
)
def identity_management_users_enable(user_id: str = None, user_ids: list = None):
    # This tool is generated using Britive SDK v4.3.0
    """Enable the given user(s).

    You can pass in both `user_id` for a single user and `user_ids` to enable multiple users in one call. If both
    `user_id` and `user_ids` are provided they will be merged together into one list.

    :param user_id: The ID of the user you wish to enable.
    :param user_ids: A list of user IDs that you wish to enable.
    :return: if `user_ids` is set will return a list of user records, else returns a user dict"""

    try:
        client = client_wrapper.get_client()
        return client.identity_management.users.enable(user_id, user_ids)
    except UnauthorizedRequest:
        raise UnauthorizedRequest(
            "User is not authenticated. Please ask the user to run `pybritive login` in their terminal to log in interactively. "
            "After the user finishes logging in, ask them to confirm so you can retry this tool."
        )


@mcp.tool(
    name="identity_management_users_disable",
    description="""Use this tool **only if the user has confirmed they are referring to user identities**. Do not assume the type of identity.Checks the status of the specified user identity. If the status is active, prompts the user for confirmation to disable it. If confirmed, it performs the disable action. If the identity is already inactive, it informs the user and suggests enabling it instead.""",
)
def identity_management_users_disable(user_id: str = None, user_ids: list = None):
    # This tool is generated using Britive SDK v4.3.0
    """Disable the given user(s).

    You can pass in both `user_id` for a single user and `user_ids` to disable multiple users at in one call.
    If both `user_id` and `user_ids` are provided they will be merged together into one list.

    :param user_id: The ID of the user you wish to disable.
    :param user_ids: A list of user IDs that you wish to disable.
    :return: if `user_ids` is set will return a list of user records, else returns a user dict"""

    try:
        client = client_wrapper.get_client()
        return client.identity_management.users.disable(user_id, user_ids)
    except UnauthorizedRequest:
        raise UnauthorizedRequest(
            "User is not authenticated. Please ask the user to run `pybritive login` in their terminal to log in interactively. "
            "After the user finishes logging in, ask them to confirm so you can retry this tool."
        )


@mcp.tool(name="identity_management_users_list", description="""Use this tool **only if the user has confirmed they are referring to user identities**. Do not assume the type of identity.This tool lists all user identities available in the Britive platform with optional filters. It provides list of details such as userID, username, type, status, email, firstName, lastName. Use this tool to get userId based on filter options and use this id in further operations like enabling or disabling a service identity. You can filter the list by username, type, status, and tags to narrow down the results.""")
def identity_management_users_list(filter_expression: str = None, include_tags: bool = False):
    # This tool is generated using Britive SDK v4.3.0
    """Provide an optionally filtered list of all users.

:param filter_expression: filter list of users based on name, status, or role. The supported operators
     are 'eq' and 'co'. Example: 'name co "Smith"'
:param include_tags: if this is set to true, tags/group memberships are returned.
:return: List of user records"""

    try:
        client = client_wrapper.get_client()
        return client.identity_management.users.list(filter_expression, include_tags)
    except UnauthorizedRequest:
        raise UnauthorizedRequest(
            "User is not authenticated. Please ask the user to run `pybritive login` in their terminal to log in interactively. "
            "After the user finishes logging in, ask them to confirm so you can retry this tool."
        )
    

@mcp.tool(name="identity_management_users_get", description="""Use this tool **only if the user has confirmed they are referring to user identities**. Do not assume the type of identity.This tool retrieves detailed information about a specific user identity by its userID. It provides comprehensive details including the identity's userId, username, email, firstName, lastName, type, status, created, modified, identityProvider and userTags. Use this tool to gather specific information about a user identity before taking actions like enabling or disabling it """)
def identity_management_users_get(user_id: str):
    # This tool is generated using Britive SDK v4.3.0
    """Provide details of the given user.

:param user_id: The ID  of the user.
:return: Details of the specified user."""

    try:
        client = client_wrapper.get_client()
        return client.identity_management.users.get(user_id)
    except UnauthorizedRequest:
        raise UnauthorizedRequest(
            "User is not authenticated. Please ask the user to run `pybritive login` in their terminal to log in interactively. "
            "After the user finishes logging in, ask them to confirm so you can retry this tool."
        )
    

@mcp.tool(name="identity_management_users_search", description="""Use this tool **only if the user has confirmed they are referring to user identities**. Do not assume the type of identity.This tool searches for user identities based on a query string. It allows you to find identities by name, username, firstName, lastName, email, type, status, identityProvider or other attributes. The search results include basic details such as userId, name, type, and status. Use this tool to quickly locate user identities that match specific criteria without needing to list all identities.""")
def identity_management_users_search(search_string: str):
    # This tool is generated using Britive SDK v4.3.0
    """Search all user fields for the given `search_string`.

:param search_string: String to search.
:return: List of user records."""

    try:
        client = client_wrapper.get_client()
        return client.identity_management.users.search(search_string)
    except UnauthorizedRequest:
        raise UnauthorizedRequest(
            "User is not authenticated. Please ask the user to run `pybritive login` in their terminal to log in interactively. "
            "After the user finishes logging in, ask them to confirm so you can retry this tool."
        )
    

@mcp.tool(name="identity_management_users_enable", description="""Use this tool **only if the user has confirmed they are referring to user identities**. Do not assume the type of identity.Checks the status of the specified user identity. If the status is inactive, prompts the user for confirmation to enable it. If confirmed, it performs the enable action. If the identity is already active, it informs the user and suggests disabling it instead.""")
def identity_management_users_enable(user_id: str = None, user_ids: list = None):
    # This tool is generated using Britive SDK v4.3.0
    """Enable the given user(s).

You can pass in both `user_id` for a single user and `user_ids` to enable multiple users in one call. If both
`user_id` and `user_ids` are provided they will be merged together into one list.

:param user_id: The ID of the user you wish to enable.
:param user_ids: A list of user IDs that you wish to enable.
:return: if `user_ids` is set will return a list of user records, else returns a user dict"""

    try:
        client = client_wrapper.get_client()
        return client.identity_management.users.enable(user_id, user_ids)
    except UnauthorizedRequest:
        raise UnauthorizedRequest(
            "User is not authenticated. Please ask the user to run `pybritive login` in their terminal to log in interactively. "
            "After the user finishes logging in, ask them to confirm so you can retry this tool."
        )
    

@mcp.tool(name="identity_management_users_disable", description="""Use this tool **only if the user has confirmed they are referring to user identities**. Do not assume the type of identity.Checks the status of the specified user identity. If the status is active, prompts the user for confirmation to disable it. If confirmed, it performs the disable action. If the identity is already inactive, it informs the user and suggests enabling it instead.""")
def identity_management_users_disable(user_id: str = None, user_ids: list = None):
    # This tool is generated using Britive SDK v4.3.0
    """Disable the given user(s).

You can pass in both `user_id` for a single user and `user_ids` to disable multiple users at in one call.
If both `user_id` and `user_ids` are provided they will be merged together into one list.

:param user_id: The ID of the user you wish to disable.
:param user_ids: A list of user IDs that you wish to disable.
:return: if `user_ids` is set will return a list of user records, else returns a user dict"""

    try:
        client = client_wrapper.get_client()
        return client.identity_management.users.disable(user_id, user_ids)
    except UnauthorizedRequest:
        raise UnauthorizedRequest(
            "User is not authenticated. Please ask the user to run `pybritive login` in their terminal to log in interactively. "
            "After the user finishes logging in, ask them to confirm so you can retry this tool."
        )
    
