from converter_config.base import ToolConfig, ToolGroup

reports = ToolGroup(
    name="reports",
    tools=[
        ToolConfig(
            function_name="list",
            ai_description="""List all available reports and their metadata.
Use this tool to:
- Retrieve report names and their `reportId`s.
- Extract available filterable columns for each report.
- Understand which operators (e.g., `eq`, `co`, `gt`) are supported per column.

You must call this tool before using any `report_run_*` tool to ensure you have the correct `reportId`, column names, and operator support.
No parameters required.""",
            tool_name="reports_list",
            regenerate=True,
            ),

        ToolConfig(
            function_name="run",
            tool_name="report_run_profile_historical_access",
            ai_description="""This tool provides historical information on profiles access checked out by users

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
""",
            regenerate=True,
        ),

        ToolConfig(
            function_name="run",
            tool_name="report_run_permissions_in_profile",
            ai_description="""This tool allows to get details on what permissions are assigned to which profiles, details on the permissions, profiles associations and policies
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
""",
            regenerate=True,
        ),

        ToolConfig(
            function_name="run",
            tool_name="report_run_tag_membership",
            ai_description="""This tool allows to get details on members associated with each tag. 
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
""",
            regenerate=True,
        ),

        ToolConfig(
            function_name="run",
            tool_name="report_run_service_identities_details",
            ai_description="""This tool allows to get details on service identities. 
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
""",
            regenerate=True,
        )
    ]
)