from britive.exceptions import UnauthorizedRequest

from britive_mcp_tools.core.mcp_init import client_wrapper, mcp


@mcp.tool(
    name="my_secrets_list",
    description="""Use this tool to retrieve a list of all secrets available to the user. This tool returns detailed information about each secret including entityType, id, name, description, secretNature, path, rotationInterval, and metadata.

    This tool should be used whenever:
    - The user asks to see what secrets they have access to
    - The user wants to view a secret but hasn't provided the explicit secret path
    - You need to help the user identify which secret they want to access

    If the user requests to view a secret but does not provide a specific path, use this tool first to display available secrets, then prompt the user to specify which secret they want to view. For example: "I can see you have access to the following secrets: [list]. Please let me know which secret you'd like to view."

    The path returned by this tool is required to use the `my_secrets_view` tool.""",
)
def my_secrets_list():
    try:
        client = client_wrapper.get_client()
        if client_wrapper.obo:
            return client.my_secrets.list(
                headers={"X-On-Behalf-Of": client_wrapper.email},
            )
        else:
            return client.my_secrets.list()
    except UnauthorizedRequest:
        raise UnauthorizedRequest(
            "User is not authenticated. Please ask the user to run `pybritive login` in their terminal to log in interactively. "
            "After the user finishes logging in, ask them to confirm so you can retry this tool."
        )


@mcp.tool(
    name="my_secrets_view",
    description="""Use this tool to view the actual value/contents of a specific secret that the user has access to. This tool retrieves the secret data for a given secret path.

    Required parameter:
    - path: The full path to the secret (e.g., "/app/production/database-password"). If the user doesn't know the exact path, use the `my_secrets_list` tool first to display available secrets and their paths.

    Optional parameters:
    - justification: A reason for accessing the secret. Only include this if the secret requires approval or if the user mentions needing to provide justification.
    - otp: One-time password for additional authentication. Only include this if the secret requires MFA/OTP or if the user provides an OTP code.
    - wait_time: Time in seconds to wait between approval checks (default: 60 seconds). Use default unless user specifies otherwise.
    - max_wait_time: Maximum time in seconds to wait for approval (default: 600 seconds). Use default unless user specifies otherwise.

    When to use this tool:
    - The user explicitly requests to view, see, or retrieve a specific secret
    - The user provides a secret path and wants to access its value
    - After using `my_secrets_list`, when the user selects which secret they want to view

    When returning secret value, format value in a copy-pastable format, like a code block or artifact""",
)
def my_secrets_view(
    path: str,
    justification: str = None,
    otp: str = None,
    wait_time: int = 60,
    max_wait_time: int = 600,
):
    try:
        client = client_wrapper.get_client()
        if client_wrapper.obo:
            return client.my_secrets.view(
                path=path,
                justification=justification,
                otp=otp,
                wait_time=wait_time,
                max_wait_time=max_wait_time,
                headers={"X-On-Behalf-Of": client_wrapper.email},
            )
        else:
            return client.my_secrets.view(
                path=path,
                justification=justification,
                otp=otp,
                wait_time=wait_time,
                max_wait_time=max_wait_time,
            )
    except UnauthorizedRequest:
        raise UnauthorizedRequest(
            "User is not authenticated. Please ask the user to run `pybritive login` in their terminal to log in interactively. "
            "After the user finishes logging in, ask them to confirm so you can retry this tool."
        )
