from ..core.mcp_init import client_wrapper, mcp


@mcp.tool(
    name="my_resources_list",
    description="""
    List all resources available for checkout. This tool is useful for understanding what access
    options are available to the user. It can also be used to find the resource and profile IDs
    needed for the `checkout` tool. This tool does not require any parameters and will return a
    list of resources with their details.

    You can also help the user by filtering the list by resource type.
    To recieve the resource types available, you can call the resource list without a type, find out what the types are, then recall the tool
    """,
)
def my_resources_list(list_type: str = None):
    client = client_wrapper.get_client()
    return client.my_resources.list(
        list_type=list_type,
        headers={"X-On-Behalf-Of": client_wrapper.email}
        if client_wrapper.obo
        else None,
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

    When do you use my_access versus my_resources?

    My access is used for access to SaaS application priviledged accounts, including but not limited to:

        MongoDB
        Atlassian
        Aviatrix
        AWS
        Azure
        Databricks
        GCP
        Github
        Kubernetes
        Okta
        Oracle
        OpenShift
        SalesForce
        Saviynt
        ServiceNow
        Snowflake
        Zoom

    My resources is used for access to everything that isn't cloud or SaaS including but not limited to:

        GKE
        GoogleWorkspace
        Guac
        Linux servers
        Databases
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
    # This tool is generated using Britive SDK v4.3.0
    """Checkout a resource.

    If the resource has already been checked out this method will return the details of the checked out resource.

    If approval is required, this method will continue to check if approval has been obtained. Once the request
    is approved the resource will be checked out. Sending a `SIGINT/KeyboardInterrupt/Ctrl+C/^C` while waiting for
    the approval request to be dispositioned will withdraw the request. Sending a second `^C` immediately after
    the first will immediately exit the program.

    :param profile_id: The ID of the profile. Use `list_resources()` to obtain the eligible profiles.
    :param resource_id: The ID of the resource. Use `list_resources()` to obtain the eligible resources.
    :param include_credentials: True if tokens should be included in the response. False if the caller wishes to
        call `credentials()` at a later time. If True, the `credentials` key will be included in the response which
        contains the response from `credentials()`. Setting this parameter to `True` will result in a synchronous
        call vs. setting to `False` will allow for an async call.
    :param justification: Optional justification if checking out the resource requires approval.
    :param max_wait_time: The maximum number of seconds to wait for an approval before throwing
        an exception.
    :param otp: Optional time based one-time passcode use for step up authentication.
    :param response_template: Optional response template for formatting the checkout response.
    :param ticket_id: Optional ITSM ticket ID
    :param ticket_type: Optional ITSM ticket type or category
    :param wait_time: The number of seconds to sleep/wait between polling to check if the resource checkout
        was approved.
    :return: Details about the checked out resource, and optionally the credentials generated by the checkout.
    :raises ApprovalRequiredButNoJustificationProvided: if approval is required but no justification is provided.
    :raises ProfileApprovalRejected: if the approval request was rejected by the approver.
    :raises ProfileApprovalTimedOut: if the approval request timed out exceeded the max time as specified by the
        profile policy.
    :raises ProfileApprovalWithdrawn: if the approval request was withdrawn by the requester."""

    client = client_wrapper.get_client()
    return client.my_resources.checkout(
        profile_id=profile_id,
        resource_id=resource_id,
        headers={"X-On-Behalf-Of": client_wrapper.email}
        if client_wrapper.obo
        else None,
        include_credentials=include_credentials,
        justification=justification,
        max_wait_time=max_wait_time,
        otp=otp,
        progress_func=None,
        response_template=response_template,
        ticket_id=ticket_id,
        ticket_type=ticket_type,
        wait_time=wait_time,
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
def my_resources_checkin(
    transaction_id: str,
):
    # This tool is generated using Britive SDK v4.3.0
    """Check in a resource.

    This method will check in a previously checked out resource using the transaction ID.

    :param transaction_id: The transaction ID of the checked out resource. Use `list_checked_out_profiles()`
        to obtain the transaction IDs of currently checked out resources.
    :return: Details about the checked in resource.
    :raises ResourceNotFound: if the transaction ID does not correspond to a checked out resource."""

    client = client_wrapper.get_client()
    return client.my_resources.checkin(
        transaction_id=transaction_id,
        headers={"X-On-Behalf-Of": client_wrapper.email}
        if client_wrapper.obo
        else None,
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
    client = client_wrapper.get_client()
    return client.my_resources.list_checked_out_profiles(
        headers={"X-On-Behalf-Of": client_wrapper.email}
        if client_wrapper.obo
        else None,
    )
