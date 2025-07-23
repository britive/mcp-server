from converter.converter_config.base import ToolConfig, ToolGroup

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
            regenerate=False,
        ),

        ToolConfig(
            function_name="run",
            tool_name="report_run_user_secret_access",
            ai_description="""This tool allows information on secret assigned to users. 
This tool retrieves details of secrets assigned to users based on their identity context

Steps:
1. Use `reports_list` to find the report named 'User Secret Access'.
2. Extract its `reportId` and valid columns/operators.
3. Call this tool with that `report_id` and optional filters.

Filterable columns include: `username`, `identityType`, `secretPath`, `secretDescription`, etc.

Examples:
- `firstname sw john`
- `secretPath co /path/to/secret`

Do not add any quotes around the values, even if they contain spaces or special characters. The tool will handle them correctly.
Strictly use the operators defined in the `logs_operators` tool, such as `eq`, `sw`, `co`, etc. if having negative context in filter matching then use operator `neq`, `nco` Do not use any other operators or formats.
""",
            regenerate=True,
        ),
        ToolConfig(
            function_name="run",
            tool_name="report_run_secret_last_access",
            ai_description="""This tool provides information on secrets and when they were accessed. 
This tool retrieves information about secrets accessed by specific identities, including access timestamps. It supports queries such as identifying which secrets were accessed in the past 30 days and by whom.

Steps:
1. Use `reports_list` to find the report named 'Secret Last Access'.
2. Extract its `reportId` and valid columns/operators.
3. Call this tool with that `report_id` and optional filters.

Filterable columns include: `secretPath`, `secretDescription`, `name`, `identityType`, `secret_last_used_time`, etc.

Examples:
- `secret_last_used_time co 2023-01-01`
- `secretPath co searchExpression`

Do not add any quotes around the values, even if they contain spaces or special characters. The tool will handle them correctly.
Strictly use the operators defined in the `logs_operators` tool, such as `eq`, `sw`, `co`, etc. and if having negative context in filter matching then use operator `neq`, `nco` Do not use any other operators or formats.
""",
            regenerate=True,
        ),

        ToolConfig(
            function_name="run",
            tool_name="report_run_profiles_assigned_to_service_identities",
            ai_description="""This tool provides information to get details on who has what access to profiles, applications and environments
This tool retrieves detailed access mappings between service identities and their assigned profiles, applications, and environments within Britive. It helps determine who has access to what, allowing you to analyze identity-level access across profiles, applications, and environments, along with related metadata such as status, mapped accounts, and tags.

Steps:
1. Use `reports_list` to find the report named 'Profile Assigned to Service Identities'.
2. Extract its `reportId` and valid columns/operators.
3. Call this tool with that `report_id` and optional filters.

Filterable columns include: `name`, `email`, `type`, `application`, `applicationStatus`, `profile`, `description`, `environment`, `environmentStatus`, `mappedAccount`, `tag`

Examples:

User may ask questions such as:

-What applications does Identity "xyz" have access to via provider?
-What environments does Identity "xyz" have access to?
-What profiles does Identity "xyz" have access to?

Expected Response Format:
Answer in a structured format (e.g., tables or bullet points).
Include metadata like Application status, Environment status, Mapped Account, etc., when relevant.
Apply column-based filters precisely based on the question.

Do not add any quotes around the values, even if they contain spaces or special characters. The tool will handle them correctly.
Strictly use the operators defined in the `logs_operators` tool, such as `eq`, `sw`, `co`, etc. and if having negative context in filter matching then use operator `neq`, `nco` Do not use any other operators or formats.
""",
            regenerate=True,
        ),

        ToolConfig(
            function_name="run",
            tool_name="report_run_profile_accessed_tags",
            ai_description=""" This tool provides tags information associated with details on who has what access to applications, environments and profiles.
    This tool retrieves detailed access mappings between profiles and their associated tags, applications, and environments within Britive. It helps determine which profiles are associated with which tags, allowing you to analyze profile-level access across applications and environments, along with related metadata such as status, mapped accounts, and tags.
        

        Steps:
        1. Use `reports_list` to find the report named 'Profiles Assigned to Tags'.
        2. Extract its `reportId` and valid columns/operators.
        3. Call this tool with that `report_id` and optional filters.

        Filterable columns include: `name`, `application`, `applicationStatus`, `profile`, `description`, `environment`, `environmentStatus`

        Examples:

        User may ask questions such as:

        -What applications does tag "xyz" have access to via provider name
        -What environments does tag "xyz" have access to via provider name
        -What profiles does a tag "xyz" have access to

    Expected Response Format:
    Answer in a structured format (e.g., tables or bullet points).
    Include metadata like Application status, Environment status, Profile, etc., when relevant associated with tags.
    Apply column-based filters precisely based on the question.

    Do not add any quotes around the values, even if they contain spaces or special characters. The tool will handle them correctly.
    Strictly use the operators defined in the `logs_operators` tool, such as `eq`, `sw`, `co`, etc. and if having negative context in filter matching then use operator `neq`, `nco` Do not use any other operators or formats.
    """,
            regenerate=True,
        ),
        ToolConfig(
            function_name="run",
            tool_name="report_run_AI_identities_secret_last_access",
            ai_description=""" This tool provides information on details of AI identities with secrets last access
    This tool retrieves detailed access mappings between AI identities and their associated secrets, including last access timestamps. It helps determine which AI identities have accessed which secrets, allowing you to analyze AI identity-level access across secrets, along with related metadata such as usernames,secret path and secret description.
        Steps:
        1. Use `reports_list` to find the report named 'AI Identity Secret Last Access'.
        2. Extract its `reportId` and valid columns/operators.
        3. Call this tool with that `report_id` and optional filters.

        Filterable columns include: `username`, `firstName`, `lastName`, `identityType`, `secretPath`, `secretDescription`, `lastAccessedTime`

        Examples:

        User may ask questions such as:
        -Give me a list of AI identities that haven't been usedin the past 30 days?
        -Give me a list of AI identities whose access tokens expire in the next y days


    Expected Response Format:
    Answer in a structured format (e.g., tables or bullet points).
    Include metadata like Application status, Environment status, Profile, etc., when relevant associated with AI identities.
    Apply column-based filters precisely based on the question.

    Do not add any quotes around the values, even if they contain spaces or special characters. The tool will handle them correctly.
    Strictly use the operators defined in the `logs_operators` tool, such as `eq`, `sw`, `co`, etc. and if having negative context in filter matching then use operator `neq`, `nco` Do not use any other operators or formats.
    """,
            regenerate=True,
        ),
        ToolConfig(
            function_name="run",
            tool_name="report_run_resource_historical_access",
            ai_description=""" This tool provides information on resource checked out by users in last 90 days.
    This tool retrieves historical information on resources accessed by users in the last 90 days. It provides details such as resource name, resource type, resource origin, last accessed date, etc.

        Steps:
        1. Use `reports_list` to find the report named 'Resource Historical Access'.
        2. Extract its `reportId` and valid columns/operators.
        3. Call this tool with that `report_id` and optional filters.

        Filterable columns include: `name`, `origin`, `resourceType`, `profileName`, `permissionName`, `version`, `identityType`, `lastAccessedDate`.

        Examples:

        User may ask questions such as:
        -Give me a list of resources that are not being used in the past 30 days?
        -Which resource has been accessed by which user in the last 2 days?


    Expected Response Format:
    Answer in a structured format (e.g., tables or bullet points).
    Apply column-based filters precisely based on the question.

    Do not add any quotes around the values, even if they contain spaces or special characters. The tool will handle them correctly.
    Strictly use the operators defined in the `logs_operators` tool, such as `eq`, `sw`, `co`, etc. and if having negative context in filter matching then use operator `neq`, `nco` Do not use any other operators or formats.
    """,
            regenerate=True,
        ),
        ToolConfig(
            function_name="run",
            tool_name="report_run_resource_last_access",
            ai_description=""" This tool provides information on when a resource was used.
    This tool retrieves information about resources accessed by specific identities, including access date and days.
        Steps:
        1. Use `reports_list` to find the report named 'Resource Last Access'.
        2. Extract its `reportId` and valid columns/operators.
        3. Call this tool with that `report_id` and optional filters.

        Filterable columns include: `name`, `origin`, `resourceType`, `profileName`, `permissionName`, `version`, `identityName`,`identityType`, `lastAccessed`, `lastAccessedDate`.

        Examples:

        User may ask questions such as:
        -Give me a list of resources that are not being used in the past 30 days?
        -Which resource has been accessed by which user in the last 2 days?


    Expected Response Format:
    Answer in a structured format (e.g., tables or bullet points).
    Apply column-based filters precisely based on the question.

    Do not add any quotes around the values, even if they contain spaces or special characters. The tool will handle them correctly.
    Strictly use the operators defined in the `logs_operators` tool, such as `eq`, `sw`, `co`, etc. and if having negative context in filter matching then use operator `neq`, `nco` Do not use any other operators or formats.
    """,
            regenerate=True,
        ),
        ToolConfig(
            function_name="run",
            tool_name="report_run_resources_assigned_to_ai_identities",
            ai_description=""" This tool provides information on resources assigned to ai identities.
    This tool retrieves detailed access mappings between AI identities and their assigned resources, including resource names, types, and origin. It helps determine which AI identities have access to which resources, allowing you to analyze AI identity-level access across resources.
        Steps:
        1. Use `reports_list` to find the report named 'Resources Assigned to AI Identities'.
        2. Extract its `reportId` and valid columns/operators.
        3. Call this tool with that `report_id` and optional filters.

        Filterable columns include: `resourceName`, `origin`, `resourceType`, `profileName`, `identityName`,`identityType`.

        Examples:

        User may ask questions such as:
        -What resources does AI identity "xyz" have access to?
        -Can you list all resources assigned to AI identity "xyz"?


    Expected Response Format:
    Answer in a structured format (e.g., tables or bullet points).
    Apply column-based filters precisely based on the question.

    Do not add any quotes around the values, even if they contain spaces or special characters. The tool will handle them correctly.
    Strictly use the operators defined in the `logs_operators` tool, such as `eq`, `sw`, `co`, etc. and if having negative context in filter matching then use operator `neq`, `nco` Do not use any other operators or formats.
    """,
            regenerate=True,
        ),
        ToolConfig(
            function_name="run",
            tool_name="report_run_resources_assigned_to_all_identities",
            ai_description=""" This tool provides information on resources assigned to all identities.
    This tool retrieves detailed access mappings between all identities and their assigned resources, including resource names, types, and origin. It helps determine which identities have access to which resources, allowing you to analyze identity-level access across resources.
        Steps:
        1. Use `reports_list` to find the report named 'Resources Assigned to All Identities'.
        2. Extract its `reportId` and valid columns/operators.
        3. Call this tool with that `report_id` and optional filters.

        Filterable columns include: `resourceName`, `origin`, `resourceType`, `profileName`, `identityName`,`identityType`.

        Examples:

        User may ask questions such as:
        -What resources does identity "xyz" have access to?
        -Can you list all resources assigned to identity "xyz"?


    Expected Response Format:
    Answer in a structured format (e.g., tables or bullet points).
    Apply column-based filters precisely based on the question.

    Do not add any quotes around the values, even if they contain spaces or special characters. The tool will handle them correctly.
    Strictly use the operators defined in the `logs_operators` tool, such as `eq`, `sw`, `co`, etc. and if having negative context in filter matching then use operator `neq`, `nco` Do not use any other operators or formats.
    """,
            regenerate=True,
        ),
        ToolConfig(
            function_name="run",
            tool_name="report_run_resources_assigned_to_service_identities",
            ai_description=""" This tool provides information on resources assigned to service identities.
    This tool retrieves detailed access mappings between service identities and their assigned resources, including resource names, types, and origin. It helps determine which service identities have access to which resources, allowing you to analyze service identity-level access across resources.
        Steps:
        1. Use `reports_list` to find the report named 'Resources Assigned to Service Identities'.
        2. Extract its `reportId` and valid columns/operators.
        3. Call this tool with that `report_id` and optional filters.

        Filterable columns include: `resourceName`, `origin`, `resourceType`, `profileName`, `identityName`,`identityType`.

        Examples:

        User may ask questions such as:
        -What resources does service identity "xyz" have access to?
        -Can you list all resources assigned to service identity "xyz"?


    Expected Response Format:
    Answer in a structured format (e.g., tables or bullet points).
    Apply column-based filters precisely based on the question.

    Do not add any quotes around the values, even if they contain spaces or special characters. The tool will handle them correctly.
    Strictly use the operators defined in the `logs_operators` tool, such as `eq`, `sw`, `co`, etc. and if having negative context in filter matching then use operator `neq`, `nco` Do not use any other operators or formats.
    """,
            regenerate=True,
        ),
        ToolConfig(
            function_name="run",
            tool_name="report_run_resources_assigned_to_tags",
            ai_description=""" This tool provides information on resources assigned to tags.
    This tool retrieves detailed access mappings between tags and their assigned resources, including resource names, types, and origin. It helps determine which tag have access to which resources, allowing you to analyze tag-level access across resources.
        Steps:
        1. Use `reports_list` to find the report named 'Resources Assigned to Tags'.
        2. Extract its `reportId` and valid columns/operators.
        3. Call this tool with that `report_id` and optional filters.

        Filterable columns include: `resourceName`, `origin`, `resourceType`, `profileName`, `identityName`,`identityType`.

        Examples:

        User may ask questions such as:
        -What resources does tag "xyz" have access to?
        -Can you list all resources assigned to tag "xyz"?


    Expected Response Format:
    Answer in a structured format (e.g., tables or bullet points).
    Apply column-based filters precisely based on the question.

    Do not add any quotes around the values, even if they contain spaces or special characters. The tool will handle them correctly.
    Strictly use the operators defined in the `logs_operators` tool, such as `eq`, `sw`, `co`, etc. and if having negative context in filter matching then use operator `neq`, `nco` Do not use any other operators or formats.
    """,
            regenerate=True,
        ),
        ToolConfig(
            function_name="run",
            tool_name="report_run_resources_assigned_to_users",
            ai_description=""" This tool provides information on resources assigned to users.
    This tool retrieves detailed access mappings between users and their assigned resources, including resource names, types, and origin. It helps determine which user have access to which resources, allowing you to analyze user-level access across resources.
        Steps:
        1. Use `reports_list` to find the report named 'Resources Assigned to Users'.
        2. Extract its `reportId` and valid columns/operators.
        3. Call this tool with that `report_id` and optional filters.

        Filterable columns include: `resourceName`, `origin`, `resourceType`, `profileName`, `identityName`,`identityType`.

        Examples:

        User may ask questions such as:
        -What resources does user "xyz" have access to?
        -Can you list all resources assigned to user "xyz"?


    Expected Response Format:
    Answer in a structured format (e.g., tables or bullet points).
    Apply column-based filters precisely based on the question.

    Do not add any quotes around the values, even if they contain spaces or special characters. The tool will handle them correctly.
    Strictly use the operators defined in the `logs_operators` tool, such as `eq`, `sw`, `co`, etc. and if having negative context in filter matching then use operator `neq`, `nco` Do not use any other operators or formats.
    """,
            regenerate=True,
        )
    ]
)