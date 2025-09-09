import datetime
from britive_mcp_tools.core.mcp_init import mcp, auth_manager
from britive.exceptions import UnauthorizedRequest
from fastmcp import Context

@mcp.tool(name="reports_list", description="""List all available reports and their metadata.
Use this tool to:
- Retrieve report names and their `reportId`s.
- Extract available filterable columns for each report.
- Understand which operators (e.g., `eq`, `co`, `gt`) are supported per column.

You must call this tool before using any `report_run_*` tool to ensure you have the correct `reportId`, column names, and operator support.
No parameters required.""")
def reports_list(ctx: Context, ):
    # This tool is generated using Britive SDK v4.3.0
    """Return list of all built-in reports.

    :return: List of reports."""

    try:
        client = auth_manager.auth_provider.get_client(ctx)
        return client.reports.list()
    except UnauthorizedRequest:
        raise UnauthorizedRequest(
            "User is not authenticated. Please ask the user to run `pybritive login` in their terminal to log in interactively. "
            "After the user finishes logging in, ask them to confirm so you can retry this tool."
        )


@mcp.tool(
    name="all_reports_run",
    description="""Run any report by specifying its `reportId` and optional filters.
Steps:
1. Use `reports_list` to find the desired report's `reportId` and valid columns/operators.
2. Call this tool with that `report_id` and optional filters.
3. If the report supports pagination, use `next_page_token` to fetch subsequent pages.
Filters should be formatted as: `columnName operator value`. E.g., `profile eq admin and application co aws`.
Supported operators include: `eq` (equals), `co` (contains), `sw` (starts with), `gt` (greater than), etc. Do not use any other operators or formats.
Do not add any quotes around the values, even if they contain spaces or special characters. The tool will handle them correctly.
""")
def all_reports_run(ctx: Context, report_id: str, csv: bool = False, filter_expression: str = None):
    # This tool is generated using Britive SDK v4.3.0
    """Run a report.

    :param report_id: The ID of the report.
    :param csv: If True the result will be returned as a CSV string. If False (default) the result will be returned
        as a list where each time in the list is a dict representing the row of data.
    :param filter_expression: The filter to apply to the report. It is left to the caller to provide a syntactically
        correct filter expression string.
    :return: CSV string or list."""

    try:
        client = auth_manager.auth_provider.get_client(ctx)
        return client.reports.run(report_id, csv, filter_expression)
    except UnauthorizedRequest:
        raise UnauthorizedRequest(
            "User is not authenticated. Please ask the user to run `pybritive login` in their terminal to log in interactively. "
            "After the user finishes logging in, ask them to confirm so you can retry this tool."
        )
    
