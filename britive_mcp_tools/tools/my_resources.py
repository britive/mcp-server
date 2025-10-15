from britive.exceptions import UnauthorizedRequest

from britive_mcp_tools.core.mcp_init import client_wrapper, mcp


@mcp.tool(
    name="my_resources_list",
    description="""
    List all resources available for checkout. This tool is useful for understanding what access 
    options are available to the user. It can also be used to find the resource and profile IDs 
    needed for the `checkout` tool. This tool does not require any parameters and will return a 
    list of resources with their details.
    """,
)
def my_resources_list():
    try:
        client = client_wrapper.get_client()
        return client.my_resources.list()
    except UnauthorizedRequest:
        raise UnauthorizedRequest(
            "User is not authenticated. Please ask the user to run `pybritive login` in their terminal to log in interactively. "
            "After the user finishes logging in, ask them to confirm so you can retry this tool."
        )


@mcp.tool(
    name="my_resources_checkout",
    description="""
    Use this tool when the user is denied access via MCP (e.g., 'access denied', 'not authorized') 
    or implicitly indicates they can't access something they should. Also trigger if the user says 
    'need access', 'get access', or refers to Britive access.

    Parameters:
    - resource_id: ID of the resource to access (infer silently from context if possible)
    - profile_id: ID of the profile to use (infer silently from context if possible)
    - programmatic: Set to True only if programmatic access is explicitly mentioned
    - justification: Include only if needed for approval (e.g., access typically restricted)
    - include_credentials: Set to True only if user expects immediate use
    - ticket_id, ticket_type, otp: Accept if provided in context (do not guess)

    Guidelines:
    1. Use list_resources tool to find resource IDs if needed
    2. If access was already granted, return it silently
    3. Handle approval flows with minimal updates unless asked
    4. For failures (rejection, timeout, withdrawal), notify with minimal friction
    5. Never use when user is only inquiring about existing access or wanting to check in

    Before checkout:
    - Try executing the prompt first
    - If execution fails, try checkout with least privilege (e.g., read-only)
    - Use administrator access only when necessary
    """,
)
def my_resources_checkout(
    profile_id: str,
    resource_id: str,
    include_credentials: bool = False,
    justification: str = None,
    max_wait_time: int = 600,
    otp: str = None,
    response_template: str = None,
    ticket_id: str = None,
    ticket_type: str = None,
    wait_time: int = 60,
):
    try:
        client = client_wrapper.get_client()
        return client.my_resources.checkout(
            profile_id,
            resource_id,
            include_credentials,
            justification,
            max_wait_time,
            otp,
            None,
            response_template,
            ticket_id,
            ticket_type,
            wait_time,
        )
    except UnauthorizedRequest:
        raise UnauthorizedRequest(
            "User is not authenticated. Please ask the user to run `pybritive login` in their terminal to log in interactively. "
            "After the user finishes logging in, ask them to confirm so you can retry this tool."
        )


@mcp.tool(
    name="my_resources_checkin",
    description="""
    Use this tool when the user has completed their task or explicitly indicates they no longer 
    need access (e.g., 'done with access', 'you can check it in', 'I'm finished', or 'revoke access').

    When to use:
    - User explicitly indicates they're done with a resource
    - User asks what access they currently have and chooses to release it
    - Need to check in all resources, not just the most recent one

    Parameters:
    - transaction_id: The only required input, identifies the resource that was previously checked out

    Guidelines:
    1. If transaction_id is not known from context, briefly ask the user
    2. Prefer silent handling unless the user expects confirmation
    3. Do not invoke preemptively unless the user's intent to end access is clear
    4. Use this tool (not the active session tools) when checking in everything
    """,
)
def my_resources_checkin(transaction_id: str):
    try:
        client = client_wrapper.get_client()
        return client.my_resources.checkin(transaction_id)
    except UnauthorizedRequest:
        raise UnauthorizedRequest(
            "User is not authenticated. Please ask the user to run `pybritive login` in their terminal to log in interactively. "
            "After the user finishes logging in, ask them to confirm so you can retry this tool."
        )


@mcp.tool(
    name="my_resources_list_checked_out_profiles",
    description="""
    Lists all currently checked-out resources for the user. Use this tool when:

    1. User asks what resources they currently have checked out
    2. User wants to know their active sessions
    3. User wants to check in a resource but doesn't remember which ones are active
    4. User needs to see transaction IDs before checking in resources
    5. User wants to verify if specific resources are checked out

    This tool requires no parameters and returns detailed information about all active resources 
    including resource names, checkout times, expiration times, and the critical transaction_id 
    needed for check-in operations.

    When to use:
    - User asks "What do I have checked out?"
    - User asks "Show me my active resources"
    - Before check-in when transaction_id is unknown
    - User needs to monitor their current access state

    The results can be used to:
    1. Inform the user about their current access
    2. Provide transaction_ids needed for the check-in tool
    3. Help determine which resources should be released
    """,
)
def my_resources_list_checked_out_profiles():
    try:
        client = client_wrapper.get_client()
        return client.my_resources.list_checked_out_profiles
    except UnauthorizedRequest:
        raise UnauthorizedRequest(
            "User is not authenticated. Please ask the user to run `pybritive login` in their terminal to log in interactively. "
            "After the user finishes logging in, ask them to confirm so you can retry this tool."
        )
