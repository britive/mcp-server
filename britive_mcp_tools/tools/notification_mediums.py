from ..core.mcp_init import client_wrapper, mcp


@mcp.tool(
    name="notification_mediums_list",
    description="""List all notification mediums configured in the Britive tenant. Returns details including ID, name, type (slack, teams, webhook), and connection parameters. Supports optional filtering by name. Use this tool to discover available notification mediums or find a specific medium's ID for use in other operations.""",
)
def notification_mediums_list(filter_expression: str = None):
    """List all notification mediums.

    :param filter_expression: Filter based on `name`. Example: `name co britive`.
    :return: List of all notification mediums."""

    client = client_wrapper.get_client()
    return client.global_settings.notification_mediums.list(filter_expression)


@mcp.tool(
    name="notification_mediums_create",
    description="""Create a new notification medium. Supports three types:
- slack: requires url and token (Auth Token for the Application BOT)
- teams: requires url (Webhook URL)
- webhook: requires url

Only provide token for slack. description is optional and will default to 'notification medium - {type}' if not provided.""",
)
def notification_mediums_create(
    notification_medium_type: str,
    name: str,
    url: str,
    token: str = None,
    description: str = None,
):
    """Create a new notification medium.

    :param notification_medium_type: the type of the notification medium - [slack, teams, webhook]
    :param name: the name of the notification medium
    :param url: the notification medium target URL
    :param token: **slack only** the Auth Token for the Application BOT
    :param description: the description of the notification medium
    :return: Details of the newly created notification medium."""

    client = client_wrapper.get_client()
    return client.global_settings.notification_mediums.create(
        notification_medium_type=notification_medium_type,
        name=name,
        url=url,
        token=token,
        description=description,
    )


@mcp.tool(
    name="notification_mediums_get",
    description="""Retrieve detailed information about a specific notification medium by its ID. Returns full details including name, type, description, and connection parameters. Use notification_mediums_list to find the ID if needed.""",
)
def notification_mediums_get(notification_medium_id: str):
    """Provide details of the given notification medium.

    :param notification_medium_id: The ID of the notification medium.
    :return: Details of the specified notification medium."""

    client = client_wrapper.get_client()
    return client.global_settings.notification_mediums.get(notification_medium_id)


@mcp.tool(
    name="notification_mediums_update",
    description="""Update an existing notification medium. Pass only the fields you want to change in the parameters dict. Valid fields:
- name: the name of the notification medium
- description: the description of the notification medium
- connectionParameters: connection settings (URL for slack/webhook, Webhook URL for teams, token for slack BOT auth)

Use notification_mediums_list to find the notification_medium_id if needed.""",
)
def notification_mediums_update(notification_medium_id: str, parameters: dict):
    """Update a notification medium.

    :param notification_medium_id: The ID of the notification medium.
    :param parameters: Parameters to update (name, description, connectionParameters).
    :return: Details of the updated notification medium."""

    client = client_wrapper.get_client()
    return client.global_settings.notification_mediums.update(notification_medium_id, parameters)


@mcp.tool(
    name="notification_mediums_delete",
    description="""Delete a notification medium by its ID. This action is permanent. Use notification_mediums_list to find the ID if needed.""",
)
def notification_mediums_delete(notification_medium_id: str):
    """Delete a notification medium.

    :param notification_medium_id: the ID of the notification medium
    :return: None"""

    client = client_wrapper.get_client()
    return client.global_settings.notification_mediums.delete(notification_medium_id)


@mcp.tool(
    name="notification_mediums_get_channels",
    description="""List all channels available for a Slack notification medium. Only applicable to Slack-type notification mediums. Use notification_mediums_list to find the notification_medium_id if needed.""",
)
def notification_mediums_get_channels(notification_medium_id: str):
    """List all channels for the given notification medium (Slack only).

    :param notification_medium_id: The ID of the notification medium.
    :return: List of all channels for the given notification medium."""

    client = client_wrapper.get_client()
    return client.global_settings.notification_mediums.get_channels(notification_medium_id)
