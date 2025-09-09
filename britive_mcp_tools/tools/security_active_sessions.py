import datetime
from britive_mcp_tools.core.mcp_init import mcp, auth_manager
from britive.exceptions import UnauthorizedRequest
from fastmcp import Context

@mcp.tool(name="security_active_sessions_list_users", description="""Lists all users on the Britive platform with active sessions in applications or resources. Returns user details including userId, name, userType, email, username, countOfProfiles, and lastLogin. Use this tool to search for a user and retrieve their userId, which can be used in follow-up operations such as retrieving the Profile Application ID (papID).""")
def security_active_sessions_list_users(ctx: Context, search_text: str = None):
    # This tool is generated using Britive SDK v4.3.0
    """Retrieve a list of users with active session(s), i.e. checked out profiles.

:return: List of users with active session(s)."""

    try:
        client = auth_manager.auth_provider.get_client(ctx)
        return client.security.active_sessions.list_users(search_text)
    except UnauthorizedRequest:
        raise UnauthorizedRequest(
            "User is not authenticated. Please ask the user to run `pybritive login` in their terminal to log in interactively. "
            "After the user finishes logging in, ask them to confirm so you can retry this tool."
        )
    

@mcp.tool(name="security_active_sessions_list_user_sessions", description="""This tool list all active session i.e. checkedout profiles for a user in the Britive platform. It returns details such as papId, profileName, description, transactionId, status, checkedOut, expiration, environmentID, EnvironmentName, accessType, appContainerId, appName, appType as part of applications list. Use this tool once you get userId and from that userId you will get all profiles associated with that user. Use this tool after obtaining the userId to fetch all profiles currently checked out by the user. This is typically used before invoking checkin or checkin_all operations to identify which sessions are active""")
def security_active_sessions_list_user_sessions(ctx: Context, user_id: str):
    # This tool is generated using Britive SDK v4.3.0
    """Retrieve the active sessions (checked out profiles) of a given user.

:param user_id: The target user's ID.
:return: Dict of the user's active Application and Resources sessions."""

    try:
        client = auth_manager.auth_provider.get_client(ctx)
        return client.security.active_sessions.list_user_sessions(user_id)
    except UnauthorizedRequest:
        raise UnauthorizedRequest(
            "User is not authenticated. Please ask the user to run `pybritive login` in their terminal to log in interactively. "
            "After the user finishes logging in, ask them to confirm so you can retry this tool."
        )
    

@mcp.tool(name="security_active_sessions_checkin", description="""This Tool will take userId and list of papID i.e. profile application ID and checkin the profile application ID for the user.It will return a message indicating whether the check-in was successful or if there were any issues.This tool should not be used when a user is asking to checkin all their profiles.That should be the my_access_checkout tool.This tool should be used when the user is asking to checkin another users profiles.""")
def security_active_sessions_checkin(ctx: Context, user_id: str, profile_ids: list):
    # This tool is generated using Britive SDK v4.3.0
    """Checkin one or more active profile sessions for a given user.

:param user_id: The target user's ID.
:param profile_ids: List of target profile ID(s) to checkin.
:return: None"""

    try:
        client = auth_manager.auth_provider.get_client(ctx)
        return client.security.active_sessions.checkin(user_id, profile_ids)
    except UnauthorizedRequest:
        raise UnauthorizedRequest(
            "User is not authenticated. Please ask the user to run `pybritive login` in their terminal to log in interactively. "
            "After the user finishes logging in, ask them to confirm so you can retry this tool."
        )
    

@mcp.tool(name="security_active_sessions_checkin_all", description="""This tool checks in all active sessions for a specific user. It requires the userId to identify the user whose sessions should be checked in. The tool will return a message indicating whether the check-in was successful or if there were any issues.""")
def security_active_sessions_checkin_all(ctx: Context, user_id: str):
    # This tool is generated using Britive SDK v4.3.0
    """Checkin all active profiles sessions for a given user.

:param user_id: The target user's ID
:return: None"""

    try:
        client = auth_manager.auth_provider.get_client(ctx)
        return client.security.active_sessions.checkin_all(user_id)
    except UnauthorizedRequest:
        raise UnauthorizedRequest(
            "User is not authenticated. Please ask the user to run `pybritive login` in their terminal to log in interactively. "
            "After the user finishes logging in, ask them to confirm so you can retry this tool."
        )
    
