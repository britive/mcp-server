from converter_config.base import ToolConfig, ToolGroup

reports = ToolGroup(
    name="reports",
    tools=[
        ToolConfig(
            function_name="list",
            ai_description="""Use this tool to list all available reports.
This tool is useful for finding report IDs, viewing available columns, and understanding supported operators.
This tool does not require any parameters and will return a list of reports with their reportsId.""",
            tool_name="reports_list",
            ),

        ToolConfig(
            function_name="run",
            tool_name="report_run_profile_historical_access",
            ai_description="""This tool provides historical information on profiles access checked out by users

Required Step Before Use:
You must first call the `reports_list` tool to:
1. Search for the report with name 'Profile Historical access'
2. Extract its `reportId` from the returned result
3. Provide that value in the `report_id` field when calling this tool

Optional: Call `logs_operators` to understand operator meanings if needed.

Filter fields: Use column names like `profileName`, `application`, `username`, etc.  
You can check available columns directly in the `columns` field of the matching report object returned from `reports_list`.

Filter formats:
1. Single column: `columnName operator value`  
   Example: `profileName eq john`
2. Multiple columns: `column1 op1 value1 and column2 op2 value2`  
   Example: `profileName eq john and application co aws`
3. Do not add any quotes around the values, even if they contain spaces or special characters. The tool will handle them correctly.
4. Strictly use the operators defined in the `logs_operators` tool, such as `eq`, `co`, `gt`, etc. Do not use any other operators or formats.
""",
        ),

        ToolConfig(
            function_name="run",
            tool_name="report_run_permissions_in_profile",
            ai_description="""This tool allows to get details on what permissions are assigned to which profiles, details on the permissions, profiles associations and policies
This tool provides information on permissions in a specific profile.

Required Step Before Use:
You must first call the `reports_list` tool to:
1. Search for the report with name 'Permissions in Profile'
2. Extract its `reportId` from the returned result
3. Provide that value in the `report_id` field when calling this tool

Optional: Call `logs_operators` to understand operator meanings if needed.

Filter fields: Use column names like `profile`, `application`, `environment`, etc.  
You can check available columns directly in the `columns` field of the matching report object returned from `reports_list`.

Filter formats:
1. Single column: `columnName operator value`  
   Example: `profile eq john`
2. Multiple columns: `column1 op1 value1 and column2 op2 value2`  
   Example: `profile eq john and application co aws`
3. Do not add any quotes around the values, even if they contain spaces or special characters. The tool will handle them correctly.
4. Strictly use the operators defined in the `logs_operators` tool, such as `eq`, `co`, `gt`, etc. Do not use any other operators or formats.
""",
        ),

        ToolConfig(
            function_name="run",
            tool_name="report_run_tag_membership",
            ai_description="""This tool allows to get details on members associated with each tag. 
This tool provides information on tag membership, including which profiles are associated with which tags. 

Required Step Before Use:
You must first call the `reports_list` tool to:
1. Search for the report with name 'Tag Membership'
2. Extract its `reportId` from the returned result
3. Provide that value in the `report_id` field when calling this tool

Optional: Call `logs_operators` to understand operator meanings if needed.

Filter fields: Use column names like `tagName`, `tagStatus`, `userName`, `userEmail`, etc.  
You can check available columns directly in the `columns` field of the matching report object returned from `reports_list`.

Filter formats:
1. Single column: `columnName operator value`  
   Example: `userName eq john`
2. Multiple columns: `column1 op1 value1 and column2 op2 value2`  
   Example: `userName eq john and tagStatus eq Active`
3. Do not add any quotes around the values, even if they contain spaces or special characters. The tool will handle them correctly.
4. Strictly use the operators defined in the `logs_operators` tool, such as `eq`, `co`, `gt`, etc. Do not use any other operators or formats.
""",
        ),

        ToolConfig(
            function_name="run",
            tool_name="report_run_service_identities_details",
            ai_description="""This tool allows to get details on service identities. 
This tool provides information on service identities and their creation and expiration dates.

Required Step Before Use:
You must first call the `reports_list` tool to:
1. Search for the report with name 'Service Identities Details'
2. Extract its `reportId` from the returned result
3. Provide that value in the `report_id` field when calling this tool

Optional: Call `logs_operators` to understand operator meanings if needed.

Filter fields: Use column names like `name`, `created`, `expiringOn`, `lastLogin`, etc.  
You can check available columns directly in the `columns` field of the matching report object returned from `reports_list`.

Filter formats:
1. Single column: `columnName operator value`  
   Example: `name eq john`
2. Multiple columns: `column1 op1 value1 and column2 op2 value2`  
   Example: `name eq john and status eq Active`
3. Do not add any quotes around the values, even if they contain spaces or special characters. The tool will handle them correctly.
4. Strictly use the operators defined in the `logs_operators` tool, such as `eq`, `co`, `gt`, etc. Do not use any other operators or formats.
""",
        )
    ]
)