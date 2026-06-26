from britive.exceptions import (
    ApprovalRequiredButNoJustificationProvided,
    ProfileCheckoutAlreadyApproved,
)

from ..core.mcp_init import client_wrapper, mcp


def _obo_headers():
    """Return the On-Behalf-Of header dict when running in OBO mode, else None."""
    return {"X-On-Behalf-Of": client_wrapper.email} if client_wrapper.obo else None


def _granted_response(my_resources, transaction, include_credentials, status, response_template=None, headers=None):
    """Build the response for a granted checkout without blocking on credential provisioning.

    A freshly checked-out resource is often returned in a `checkOutSubmitted` state while access is
    still being provisioned. Fetching credentials in that window blocks (and can raise) until the
    transaction flips to `checkedOut`. So we attach credentials only when the transaction is already
    `checkedOut`; otherwise we return a `provisioning` status and let the caller poll again.
    """
    txn = transaction or {}
    if include_credentials and txn.get("status") == "checkedOut":
        txn = dict(txn)
        txn["credentials"] = my_resources.credentials(
            transaction_id=txn.get("transactionId"), response_template=response_template, headers=headers
        )
        return {"status": status, "transaction": txn}
    if include_credentials:
        return {
            "status": "provisioning",
            "transaction_id": txn.get("transactionId"),
            "transaction": txn,
            "message": "Access was granted but credentials are still being provisioned. Poll the "
            "status tool (or re-run checkout) again shortly to retrieve them.",
        }
    return {"status": status, "transaction": txn}


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
    3. This tool is ASYNCHRONOUS and never blocks. Check the returned "status":
       - "checked_out": access granted immediately; the 'transaction' holds the details (and credentials if requested).
       - "justification_required": approval is needed but no justification was supplied; ask the user for one and call again.
       - "pending_approval": an approval request was submitted; a 'request_id' is returned. Inform the user once, then poll `my_resources_checkout_status` with that request_id to obtain credentials once approved. Do not loop rapidly.
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
    otp: str = None,
    response_template: str = None,
    ticket_id: str = None,
    ticket_type: str = None,
):
    """Asynchronously check out a resource.

    Unlike the blocking SDK `checkout()`, this tool never waits for an approval to be dispositioned. Instead
    it returns immediately with a status the caller can act on:

    - If the resource is already checked out or requires no approval, the checkout is performed and the
      transaction (optionally including credentials) is returned with status "checked_out".
    - If approval is required and a justification was provided, a non-blocking approval request is submitted
      and status "pending_approval" is returned along with the request_id to poll via `my_resources_checkout_status`.
    - If approval is required but no justification was provided, status "justification_required" is returned.

    :param profile_id: The ID of the profile. Use `list_resources()` to obtain the eligible profiles.
    :param resource_id: The ID of the resource. Use `list_resources()` to obtain the eligible resources.
    :param include_credentials: True if tokens should be included in the response when access is granted.
    :param justification: Justification required if checking out the resource requires approval.
    :param otp: Optional time based one-time passcode used for step up authentication.
    :param response_template: Optional response template for formatting the checkout response.
    :param ticket_id: Optional ITSM ticket ID
    :param ticket_type: Optional ITSM ticket type or category
    :return: A dict with a "status" key (one of "checked_out", "pending_approval", "justification_required")."""

    client = client_wrapper.get_client()
    headers = _obo_headers()
    try:
        # Probe with the real checkout but force an immediate failure (rather than a blocking poll)
        # if approval is required, by withholding the justification on this attempt. The failed
        # checkout does not create an approval request -- that is a separate endpoint invoked below.
        transaction = client.my_resources.checkout(
            profile_id=profile_id,
            resource_id=resource_id,
            headers=headers,
            include_credentials=False,
            justification=None,
            otp=otp,
            progress_func=None,
            response_template=response_template,
            ticket_id=ticket_id,
            ticket_type=ticket_type,
        )
        return _granted_response(
            client.my_resources, transaction, include_credentials, "checked_out", response_template, headers
        )
    except ApprovalRequiredButNoJustificationProvided:
        if not justification:
            return {
                "status": "justification_required",
                "profile_id": profile_id,
                "resource_id": resource_id,
                "message": "This resource requires approval. Ask the user for a justification, then call "
                "my_resources_checkout again with the justification provided.",
            }
        try:
            request = client.my_resources.request_approval(
                justification=justification,
                profile_id=profile_id,
                resource_id=resource_id,
                block_until_disposition=False,
                ticket_id=ticket_id,
                ticket_type=ticket_type,
                headers=headers,
            )
        except ProfileCheckoutAlreadyApproved:
            # Approval already granted out-of-band -- the checkout will now succeed.
            transaction = client.my_resources.checkout(
                profile_id=profile_id,
                resource_id=resource_id,
                headers=headers,
                include_credentials=False,
                progress_func=None,
                response_template=response_template,
            )
            return _granted_response(
                client.my_resources, transaction, include_credentials, "checked_out", response_template, headers
            )
        request_id = request.get("requestId") if isinstance(request, dict) else None
        return {
            "status": "pending_approval",
            "request_id": request_id,
            "profile_id": profile_id,
            "resource_id": resource_id,
            "include_credentials": include_credentials,
            "response_template": response_template,
            "message": "Approval has been requested. Poll my_resources_checkout_status with this request_id "
            "to check the outcome and obtain credentials once approved.",
        }


@mcp.tool(
    name="my_resources_checkout_status",
    description="""Check the status of an approval-required resource checkout that was previously submitted via `my_resources_checkout` (which returned status "pending_approval" and a request_id).

    Call this tool to poll the outcome of a pending approval. Provide the 'request_id' returned by `my_resources_checkout`, along with the same 'profile_id', 'resource_id', 'include_credentials', and 'response_template' values used in the original checkout.

    The response 'status' will be one of:
    - "pending": approval has not yet been dispositioned. Wait a bit, then call this tool again. Do not poll rapidly.
    - "approved": access was granted. The resource is now checked out and the 'transaction' (with credentials if requested) is returned. You are done.
    - "provisioning": approval was granted and checkout has started, but credentials are not ready yet. Wait briefly and call this tool again to retrieve them.
    - "rejected" / "timeout" / "cancelled": the request will not be fulfilled. Inform the user with minimal friction.

    Do not use this tool to check existing/active access -- it is only for polling a pending approval request.""",
)
def my_resources_checkout_status(
    request_id: str,
    profile_id: str,
    resource_id: str,
    include_credentials: bool = False,
    response_template: str = None,
):
    """Poll the status of a pending resource-checkout approval request and finalize the checkout once approved.

    :param request_id: The approval request ID returned by `my_resources_checkout` with status "pending_approval".
    :param profile_id: The ID of the profile being checked out.
    :param resource_id: The ID of the resource being checked out.
    :param include_credentials: True if tokens should be included in the response once approved.
    :param response_template: Optional response template for formatting the checkout response.
    :return: A dict with a "status" key (one of "pending", "approved", "rejected", "timeout", "cancelled")."""

    client = client_wrapper.get_client()
    headers = _obo_headers()
    details = client.my_requests.approval_request_status(request_id=request_id, headers=headers)
    status = (details.get("status") or "").lower() if isinstance(details, dict) else ""

    if status == "pending":
        return {
            "status": "pending",
            "request_id": request_id,
            "message": "Approval is still pending. Wait before polling again.",
        }

    if status == "approved":
        # Approval granted -- the checkout now succeeds without blocking. Fetch credentials only
        # once provisioning completes (status checkedOut); otherwise report "provisioning".
        transaction = client.my_resources.checkout(
            profile_id=profile_id,
            resource_id=resource_id,
            headers=headers,
            include_credentials=False,
            progress_func=None,
            response_template=response_template,
        )
        return _granted_response(
            client.my_resources, transaction, include_credentials, "approved", response_template, headers
        )

    # rejected / timeout / cancelled
    return {
        "status": status or "unknown",
        "request_id": request_id,
        "details": details,
        "message": f"Approval request is '{status or 'unknown'}'. Access will not be granted for this request.",
    }


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
