from britive.exceptions import (
    ApprovalRequiredButNoJustificationProvided,
    ProfileCheckoutAlreadyApproved,
)
from britive.exceptions.badrequest import PendingProfileApprovalRequestError

from britive_mcp_tools.core.mcp_init import client_wrapper, mcp


def _obo_headers():
    """Return the On-Behalf-Of header dict when running in OBO mode, else None."""
    return {"X-On-Behalf-Of": client_wrapper.email} if client_wrapper.obo else None


def _granted_response(my_access, transaction, include_credentials, status, headers=None):
    """Build the response for a granted checkout without blocking on credential provisioning.

    A freshly checked-out profile is often returned in a `checkOutSubmitted` state while access is
    still being provisioned. Fetching credentials in that window blocks (and can raise) until the
    transaction flips to `checkedOut`. So we attach credentials only when the transaction is already
    `checkedOut`; otherwise we return a `provisioning` status and let the caller poll again.
    """
    txn = transaction or {}
    if include_credentials and txn.get("status") == "checkedOut":
        txn = dict(txn)
        txn["credentials"] = my_access.credentials(transaction_id=txn.get("transactionId"), headers=headers)
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
    name="my_access_checkout",
    description="""Use this tool when the user is denied access via MCP (e.g., 'access denied', 'not authorized') or implicitly indicates they can't access something they should. Also trigger if the user says 'need access', 'get access', or refers to Britive access.

    Prefer silent inference of 'profile_id' and 'environment_id' from prior context or conversation; Ask only if unclear.

    Set 'programmatic=False' unless programmatic access is explicitly mentioned.

    Include 'justification' only if needed for approval (e.g., access typically restricted or user says 'need approval').

    Use 'include_credentials=True' only if the user expects immediate use. If there is a console URL generated, create a clickable link for the user.

    Accept optional 'ticket_id', 'ticket_type', or 'otp' if context provides them. Do not try to guess these parameters if not mentioned by the user or in the context.

    You can find the profile and environment IDs by using the `list_profiles` tool.

    THIS TOOL IS ASYNCHRONOUS AND NEVER BLOCKS. It returns one of these statuses in the response:
    - "checked_out": access was granted immediately (no approval required, or already checked out). The 'transaction' holds the details (and credentials if requested). You are done.
    - "justification_required": the profile requires approval but no justification was supplied. Ask the user for a justification, then call this tool again with it.
    - "pending_approval": an approval request was submitted. The response includes a 'request_id'. Do NOT block or loop here. Inform the user once that approval is pending, then call `my_access_checkout_status` with the returned request_id (and the same profile_id/environment_id/include_credentials/programmatic) to check the outcome and obtain credentials once approved. Poll that tool periodically rather than rapidly.

    If access was already granted, return it silently. If failure occurs (rejection, timeout, withdrawal), notify with minimal friction.

    Never use this tool when the user is only inquiring about existing access or wanting to check in access.

    Before attempting a checkout, try to execute the prompt. If the execution fails try a checkout, but ensure that least privilege access is used. As an example, if the needed permissions for the prompt require read only access just checkout the profile for read only access. Only do administrator when needed.

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
def my_access_checkout(
    profile_id: str,
    environment_id: str,
    include_credentials: bool = False,
    justification: str = None,
    otp: str = None,
    programmatic: bool = False,
    ticket_id: str = None,
    ticket_type: str = None,
):
    """Asynchronously check out a profile.

    Unlike the blocking SDK `checkout()`, this tool never waits for an approval to be dispositioned. Instead
    it returns immediately with a status the caller can act on:

    - If the profile is already checked out or requires no approval, the checkout is performed and the
      transaction (optionally including credentials) is returned with status "checked_out".
    - If approval is required and a justification was provided, a non-blocking approval request is submitted
      and status "pending_approval" is returned along with the request_id to poll via `my_access_checkout_status`.
    - If approval is required but no justification was provided, status "justification_required" is returned.

    :param profile_id: The ID of the profile. Use `list_profiles()` to obtain the eligible profiles.
    :param environment_id: The ID of the environment. Use `list_profiles()` to obtain the eligible environments.
    :param include_credentials: True if tokens should be included in the response when access is granted.
    :param justification: Justification required if checking out the profile requires approval.
    :param otp: Optional time based one-time passcode used for step up authentication.
    :param programmatic: True for programmatic credential checkout. False for console checkout.
    :param ticket_id: Optional ITSM ticket ID
    :param ticket_type: Optional ITSM ticket type or category
    :return: A dict with a "status" key (one of "checked_out", "pending_approval", "justification_required")."""

    client = client_wrapper.get_client()
    headers = _obo_headers()
    try:
        # Probe with the real checkout but force an immediate failure (rather than a blocking poll)
        # if approval is required, by withholding the justification on this attempt. The failed
        # checkout does not create an approval request -- that is a separate endpoint invoked below.
        transaction = client.my_access.checkout(
            profile_id=profile_id,
            environment_id=environment_id,
            headers=headers,
            include_credentials=False,
            justification=None,
            otp=otp,
            programmatic=programmatic,
            progress_func=None,
            ticket_id=ticket_id,
            ticket_type=ticket_type,
        )
        return _granted_response(client.my_access, transaction, include_credentials, "checked_out", headers)
    except PendingProfileApprovalRequestError:
        # An approval request for this profile/environment is already outstanding. Report it as
        # pending (instead of surfacing the raw 400) so the caller polls status rather than resubmitting.
        return {
            "status": "pending_approval",
            "request_id": None,
            "profile_id": profile_id,
            "environment_id": environment_id,
            "include_credentials": include_credentials,
            "programmatic": programmatic,
            "message": "An approval request is already pending for this profile/environment. Poll "
            "my_access_checkout_status with the request_id from the original checkout; do not submit another.",
        }
    except ApprovalRequiredButNoJustificationProvided:
        if not justification:
            return {
                "status": "justification_required",
                "profile_id": profile_id,
                "environment_id": environment_id,
                "message": "This profile requires approval. Ask the user for a justification, then call "
                "my_access_checkout again with the justification provided.",
            }
        try:
            request = client.my_access.request_approval(
                profile_id=profile_id,
                justification=justification,
                environment_id=environment_id,
                block_until_disposition=False,
                ticket_id=ticket_id,
                ticket_type=ticket_type,
                headers=headers,
            )
        except ProfileCheckoutAlreadyApproved:
            # Approval already granted out-of-band -- the checkout will now succeed.
            transaction = client.my_access.checkout(
                profile_id=profile_id,
                environment_id=environment_id,
                headers=headers,
                include_credentials=False,
                programmatic=programmatic,
                progress_func=None,
            )
            return _granted_response(client.my_access, transaction, include_credentials, "checked_out", headers)
        request_id = request.get("requestId") if isinstance(request, dict) else None
        return {
            "status": "pending_approval",
            "request_id": request_id,
            "profile_id": profile_id,
            "environment_id": environment_id,
            "include_credentials": include_credentials,
            "programmatic": programmatic,
            "message": "Approval has been requested. Poll my_access_checkout_status with this request_id "
            "to check the outcome and obtain credentials once approved.",
        }


@mcp.tool(
    name="my_access_checkout_status",
    description="""Check the status of an approval-required profile checkout that was previously submitted via `my_access_checkout` (which returned status "pending_approval" and a request_id).

    Call this tool to poll the outcome of a pending approval. Provide the 'request_id' returned by `my_access_checkout`, along with the same 'profile_id', 'environment_id', 'include_credentials', and 'programmatic' values used in the original checkout.

    The response 'status' will be one of:
    - "pending": approval has not yet been dispositioned. Wait a bit, then call this tool again. Do not poll rapidly.
    - "approved": access was granted. The profile is now checked out and the 'transaction' (with credentials if requested) is returned. You are done.
    - "provisioning": approval was granted and checkout has started, but credentials are not ready yet. Wait briefly and call this tool again to retrieve them.
    - "rejected" / "timeout" / "cancelled": the request will not be fulfilled. Inform the user with minimal friction.

    Do not use this tool to check existing/active access -- it is only for polling a pending approval request.""",
)
def my_access_checkout_status(
    request_id: str,
    profile_id: str,
    environment_id: str,
    include_credentials: bool = False,
    programmatic: bool = False,
):
    """Poll the status of a pending profile-checkout approval request and finalize the checkout once approved.

    :param request_id: The approval request ID returned by `my_access_checkout` with status "pending_approval".
    :param profile_id: The ID of the profile being checked out.
    :param environment_id: The ID of the environment being checked out.
    :param include_credentials: True if tokens should be included in the response once approved.
    :param programmatic: True for programmatic credential checkout. False for console checkout.
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
        transaction = client.my_access.checkout(
            profile_id=profile_id,
            environment_id=environment_id,
            headers=headers,
            include_credentials=False,
            programmatic=programmatic,
            progress_func=None,
        )
        return _granted_response(client.my_access, transaction, include_credentials, "approved", headers)

    # rejected / timeout / cancelled
    return {
        "status": status or "unknown",
        "request_id": request_id,
        "details": details,
        "message": f"Approval request is '{status or 'unknown'}'. Access will not be granted for this request.",
    }


@mcp.tool(
    name="my_access_checkin",
    description="""Use this tool when the user has completed their task or explicitly indicates they no longer need access(e.g., 'done with access', 'you can check it in', 'I'm finished', or 'revoke access').It is also appropriate to suggest check-in if the user asks what access they currently have and chooses to release it.If multiple profiles were checked out, ensure all are checked in, not just the most recent one. Prefer silent handling unless the user expects confirmation.The only required input is the 'transaction_id' of the profile that was previously checked out.If not already tracked or known from context, ask the user briefly.Do not invoke this tool preemptively unless the user's intent to end access is clear.If you are asking to checkin everything, use this tool, not the active session tools.""",
)
def my_access_checkin(transaction_id: str):
    # This tool is generated using Britive SDK v4.3.0
    """Check in a checked out profile.

    :param transaction_id: The ID of the transaction.
    :return: Details of the checked in profile."""

    client = client_wrapper.get_client()
    return client.my_access.checkin(
        transaction_id=transaction_id,
        headers={"X-On-Behalf-Of": client_wrapper.email}
        if client_wrapper.obo
        else None,
    )


@mcp.tool(
    name="my_access_list_profiles",
    description="""List all profiles available for checkout. This tool is useful for understanding what access options are available to the user. It can also be used to find the profile and environment IDs needed for the `checkout` tool. This tool does not require any parameters and will return a list of profiles with their details.""",
)
def my_access_list_profiles():
    # This tool is generated using Britive SDK v4.3.0
    """List the profiles for which the user has access.

    :return: List of profiles."""

    client = client_wrapper.get_client()
    return client.my_access.list_profiles(
        headers={"X-On-Behalf-Of": client_wrapper.email}
        if client_wrapper.obo
        else None,
    )


@mcp.tool(
    name="my_access_whoami",
    description="""
Use this tool to retrieve details of the currently authenticated identity (user or service).
It returns information like username, type (user/service), and any other associated metadata.

When to Use:
- When the user asks questions like:
  - "Who am I?"
  - "What user is currently logged in?"
  - "Tell me about my account"
  - "What is my identity?"

- When the user refers to themselves using:
  - Words like "I", "me", "my", "mine"
  - Phrases that imply a self-reference (e.g., "my secrets", "my roles", "my entitlements")

- When another tool requires an identity as input, but the user did not specify one.
  - In such cases, use `whoami` first to fetch the identity, and then pass it to the next tool.

Constraints:
- Only use this tool when the user is referring to themselves.
- Do **not** use this tool when the user is asking about someone else.""",
)
def my_access_whoami():
    # This tool is generated using Britive SDK v4.3.0
    """Return details about the currently authenticated identity (user or service).

    :return: Details of the currently authenticated identity."""

    client = client_wrapper.get_client()
    return client.my_access.whoami(
        headers={"X-On-Behalf-Of": client_wrapper.email}
        if client_wrapper.obo
        else None
    )
