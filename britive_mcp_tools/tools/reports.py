import datetime
from britive_mcp_tools.core.mcp_init import mcp, client_wrapper
from britive.exceptions import UnauthorizedRequest

@mcp.tool(name="reports_list", description="""List all available reports and their metadata.
Use this tool to:
- Retrieve report names and their `reportId`s.
- Extract available filterable columns for each report.
- Understand which operators (e.g., `eq`, `co`, `gt`) are supported per column.

You must call this tool before using any `report_run_*` tool to ensure you have the correct `reportId`, column names, and operator support.
No parameters required.""")
def reports_list():
    # This tool is generated using Britive SDK v4.2.0
    """Return list of all built-in reports.

:return: List of reports."""

    try:
        client = client_wrapper.get_client()
        return client.reports.list()
    except UnauthorizedRequest:
        raise UnauthorizedRequest(
            "User is not authenticated. Please ask the user to run `pybritive login` in their terminal to log in interactively. "
            "After the user finishes logging in, ask them to confirm so you can retry this tool."
        )
    

@mcp.tool(name="report_run_profile_historical_access", description="""This tool provides historical information on profiles access checked out by users

Steps:
1. Use `reports_list` to find the report named 'Profile Historical access'.
2. Extract its `reportId` and valid columns/operators.
3. Call this tool with that `report_id` and optional filters.

Filterable columns include: `profileName`, `application`, `username`, etc.

Examples:
- `profileName eq john`
- `profileName eq john and application co aws`

Do not add any quotes around the values, even if they contain spaces or special characters. The tool will handle them correctly.
Strictly use the operators defined in the `logs_operators` tool, such as `eq`, `co`, `gt`, etc. Do not use any other operators or formats.
""")
def report_run_profile_historical_access(report_id: str, csv: bool = False, filter_expression: str = None):
    # This tool is generated using Britive SDK v4.2.0
    """Run a report.

:param report_id: The ID of the report.
:param csv: If True the result will be returned as a CSV string. If False (default) the result will be returned
    as a list where each time in the list is a dict representing the row of data.
:param filter_expression: The filter to apply to the report. It is left to the caller to provide a syntactically
    correct filter expression string.
:return: CSV string or list."""

    try:
        client = client_wrapper.get_client()
        return client.reports.run(report_id, csv, filter_expression)
    except UnauthorizedRequest:
        raise UnauthorizedRequest(
            "User is not authenticated. Please ask the user to run `pybritive login` in their terminal to log in interactively. "
            "After the user finishes logging in, ask them to confirm so you can retry this tool."
        )
    

@mcp.tool(name="report_run_permissions_in_profile", description="""This tool allows to get details on what permissions are assigned to which profiles, details on the permissions, profiles associations and policies
This tool provides information on permissions in a specific profile.

Steps:
1. Use `reports_list` to find the report named 'Permissions in Profile'.
2. Extract its `reportId` and valid columns/operators.
3. Call this tool with that `report_id` and optional filters.

Filterable columns include: `profile`, `application`, `environment`, etc.

Examples:
- `profile eq john`
- `profile eq john and application co azure`

Do not add any quotes around the values, even if they contain spaces or special characters. The tool will handle them correctly.
Strictly use the operators defined in the `logs_operators` tool, such as `eq`, `co`, `gt`, etc. Do not use any other operators or formats.
""")
def report_run_permissions_in_profile(report_id: str, csv: bool = False, filter_expression: str = None):
    # This tool is generated using Britive SDK v4.2.0
    """Run a report.

:param report_id: The ID of the report.
:param csv: If True the result will be returned as a CSV string. If False (default) the result will be returned
    as a list where each time in the list is a dict representing the row of data.
:param filter_expression: The filter to apply to the report. It is left to the caller to provide a syntactically
    correct filter expression string.
:return: CSV string or list."""

    try:
        client = client_wrapper.get_client()
        return client.reports.run(report_id, csv, filter_expression)
    except UnauthorizedRequest:
        raise UnauthorizedRequest(
            "User is not authenticated. Please ask the user to run `pybritive login` in their terminal to log in interactively. "
            "After the user finishes logging in, ask them to confirm so you can retry this tool."
        )
    

@mcp.tool(name="report_run_tag_membership", description="""This tool allows to get details on members associated with each tag. 
This tool provides information on tag membership, including which profiles are associated with which tags. 

Steps:
1. Use `reports_list` to find the report named 'Tag Membership'.
2. Extract its `reportId` and valid columns/operators.
3. Call this tool with that `report_id` and optional filters.

Filterable columns include: `tagName`, `tagStatus`, `userName`, `userEmail`, etc.

Examples:
- `userName eq john`
- `userName eq john and tagStatus co Active`

Do not add any quotes around the values, even if they contain spaces or special characters. The tool will handle them correctly.
Strictly use the operators defined in the `logs_operators` tool, such as `eq`, `co`, `gt`, etc. Do not use any other operators or formats.
""")
def report_run_tag_membership(report_id: str, csv: bool = False, filter_expression: str = None):
    # This tool is generated using Britive SDK v4.2.0
    """Run a report.

:param report_id: The ID of the report.
:param csv: If True the result will be returned as a CSV string. If False (default) the result will be returned
    as a list where each time in the list is a dict representing the row of data.
:param filter_expression: The filter to apply to the report. It is left to the caller to provide a syntactically
    correct filter expression string.
:return: CSV string or list."""

    try:
        client = client_wrapper.get_client()
        return client.reports.run(report_id, csv, filter_expression)
    except UnauthorizedRequest:
        raise UnauthorizedRequest(
            "User is not authenticated. Please ask the user to run `pybritive login` in their terminal to log in interactively. "
            "After the user finishes logging in, ask them to confirm so you can retry this tool."
        )
    

@mcp.tool(name="report_run_service_identities_details", description="""This tool allows to get details on service identities. 
This tool provides information on service identities and their creation and expiration dates.

Steps:
1. Use `reports_list` to find the report named 'Service Identities Details'.
2. Extract its `reportId` and valid columns/operators.
3. Call this tool with that `report_id` and optional filters.

Filterable columns include: `name`, `created`, `expiringOn`, `lastLogin`, etc.

Examples:
- `name eq john`
- `name eq john and status eq Active`

Do not add any quotes around the values, even if they contain spaces or special characters. The tool will handle them correctly.
Strictly use the operators defined in the `logs_operators` tool, such as `eq`, `co`, `gt`, etc. Do not use any other operators or formats.
""")
def report_run_service_identities_details(report_id: str, csv: bool = False, filter_expression: str = None):
    # This tool is generated using Britive SDK v4.2.0
    """Run a report.

:param report_id: The ID of the report.
:param csv: If True the result will be returned as a CSV string. If False (default) the result will be returned
    as a list where each time in the list is a dict representing the row of data.
:param filter_expression: The filter to apply to the report. It is left to the caller to provide a syntactically
    correct filter expression string.
:return: CSV string or list."""

    try:
        client = client_wrapper.get_client()
        return client.reports.run(report_id, csv, filter_expression)
    except UnauthorizedRequest:
        raise UnauthorizedRequest(
            "User is not authenticated. Please ask the user to run `pybritive login` in their terminal to log in interactively. "
            "After the user finishes logging in, ask them to confirm so you can retry this tool."
        )
    
