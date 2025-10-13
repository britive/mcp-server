import datetime

from britive_mcp_tools.core.mcp_init import client_wrapper, mcp
from fastmcp import Context

from britive.exceptions import UnauthorizedRequest

@mcp.tool(
    name="my_secrets_list",
    description="""List all secrets available to the user""",
)
def my_secrets_list():
    """List the secrets for which the user has access.

    :return: List of secrets."""

    try:
        client = client_wrapper.get_client()
        return client.my_secrets.list()
    except UnauthorizedRequest:
        raise UnauthorizedRequest(
            "User is not authenticated. Please ask the user to run `pybritive login` in their terminal to log in interactively. "
            "After the user finishes logging in, ask them to confirm so you can retry this tool."
        )

