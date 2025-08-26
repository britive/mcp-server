import datetime
from britive_mcp_tools.core.mcp_init import mcp, client_wrapper
from britive.exceptions import UnauthorizedRequest
from fastmcp import Context

@mcp.tool(name="audit_logs_logs_fields", description="""Call this before using query tool as it returns list of fields that can be used in a filter for an audit query.""")
def audit_logs_logs_fields(ctx: Context, ):
    # This tool is generated using Britive SDK v4.3.0
    """Return list of fields that be can used in a filter for an audit query.

:return: Dict of field keys to field names."""

    try:
        client = client_wrapper.get_client(ctx)
        return client.audit_logs.logs.fields()
    except UnauthorizedRequest:
        raise UnauthorizedRequest(
            "User is not authenticated. Please ask the user to run `pybritive login` in their terminal to log in interactively. "
            "After the user finishes logging in, ask them to confirm so you can retry this tool."
        )
    

@mcp.tool(name="audit_logs_logs_operators", description="""Call this before using query tool as it returns the list of operators that can be used in a filter for an audit query.""")
def audit_logs_logs_operators(ctx: Context, ):
    # This tool is generated using Britive SDK v4.3.0
    """Return the list of operators that can be used in a filter for an audit query.

:return: Dict of operator keys to operator names."""

    try:
        client = client_wrapper.get_client(ctx)
        return client.audit_logs.logs.operators()
    except UnauthorizedRequest:
        raise UnauthorizedRequest(
            "User is not authenticated. Please ask the user to run `pybritive login` in their terminal to log in interactively. "
            "After the user finishes logging in, ask them to confirm so you can retry this tool."
        )
    

@mcp.tool(name="audit_logs_logs_query", description="""This is used to retrieve audit log events based on the fields and operators. You need to call the `fields` and `operators` tools before using this tool to ensure you have the correct fields and operators for your query.""")
def audit_logs_logs_query(ctx: Context, from_time: datetime.datetime = None, to_time: datetime.datetime = None, filter_expression: str = None, csv: bool = False):
    # This tool is generated using Britive SDK v4.3.0
    """Retrieve audit log events.

`csv` options:

    - True: A CSV string is returned. The caller must persist the CSV string to disk.
    - False: A python list of audit events is returned.

:param from_time: Lower end of the time frame to search. If not provided will default to
    7 days before `to_time`. `from_time` will be interpreted as if in UTC timezone so it is up to the caller to
    ensure that the datetime object represents UTC. No timezone manipulation will occur.
:param to_time: Upper end of the time frame to search. If not provided will default to
    `datetime.datetime.utcnow()`. `to_time` will be interpreted as if in UTC timezone so it is up to the caller
    to ensure that the datetime object represents UTC. No timezone manipulation will occur.
:param filter_expression: The expression used to filter the results. A list of available fields and operators
    can be found using `britive.audit_logs.logs.fields` and `britive.audit_logs.logs.operators`, respectively.
    Multiple filter expressions must be joined together by `and`. No other join operator is support.
    Example: actor.displayName co "bob" and event.displayName eq "application"
:param csv: Will result in a CSV string of the audit events being returned instead of a python list of events.
:return: Either python list of events (dicts) or CSV string.
:raises: ValueError - If from_time is greater than to_time."""

    try:
        client = client_wrapper.get_client(ctx)
        return client.audit_logs.logs.query(from_time, to_time, filter_expression, csv)
    except UnauthorizedRequest:
        raise UnauthorizedRequest(
            "User is not authenticated. Please ask the user to run `pybritive login` in their terminal to log in interactively. "
            "After the user finishes logging in, ask them to confirm so you can retry this tool."
        )
    
