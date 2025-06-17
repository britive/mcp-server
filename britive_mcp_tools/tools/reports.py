import datetime

from britive_mcp_tools.core.mcp_init import client_wrapper, mcp
from fastmcp import Context

from britive.exceptions import UnauthorizedRequest


@mcp.tool(
    name="reports_list",
    description="""List all available reports and their metadata.
Use this tool to:
- Retrieve report names and their `reportId`s.
- Extract available filterable columns for each report.
- Understand which operators (e.g., `eq`, `co`, `gt`) are supported per column.

You must call this tool before using any `report_run_*` tool to ensure you have the correct `reportId`, column names, and operator support.
No parameters required.""",
)
def reports_list():
    # This tool is generated using Britive SDK v4.3.0
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


@mcp.tool(
    name="report_run_profile_historical_access",
    description="""This tool provides historical information on profiles access checked out by users

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
)
def report_run_profile_historical_access(report_id: str, csv: bool = False, filter_expression: str = None):
    # This tool is generated using Britive SDK v4.3.0
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


@mcp.tool(
    name="report_run_permissions_in_profile",
    description="""This tool allows to get details on what permissions are assigned to which profiles, details on the permissions, profiles associations and policies
This tool provides information on permissions in a specific profile.

Steps:
1. Use `reports_list` to find the report named 'Permissions in Profile'.
2. Extract its `reportId` and valid columns/operators.
3. Call this tool with that `report_id` and optional filters.
4. Once this tool returns a list of permissions, for each permission fetched:
   - Automatically call the `report_run_permission_details` tool for each permission to get **granular details**.
   - Do not call the `report_run_permission_details` tool before this tool returns the list of permissions.
          
Filterable columns include: `profile`, `application`, `environment`, etc.
Use `co` for filter as user might not know the exact name, so use `co` operator to match partial names. Avoid using `eq` operator as it requires exact match.

Examples:
- `profile eq john`
- `profile eq john and application co azure`

Do not add any quotes around the values, even if they contain spaces or special characters. The tool will handle them correctly.
Strictly use the operators defined in the `logs_operators` tool, such as `eq`, `co`, `gt`, etc. Do not use any other operators or formats.

### Important:
- This tool should be chained with `report_run_permission_details` for each permission it returns.
- The output of this tool is incomplete until detailed permission info is fetched using the second tool.
""",
)
def report_run_permissions_in_profile(report_id: str, csv: bool = False, filter_expression: str = None):
    # This tool is generated using Britive SDK v4.3.0
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


@mcp.tool(
    name="report_run_tag_membership",
    description="""This tool allows to get details on members associated with each tag. 
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
)
def report_run_tag_membership(report_id: str, csv: bool = False, filter_expression: str = None):
    # This tool is generated using Britive SDK v4.3.0
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


@mcp.tool(
    name="report_run_service_identities_details",
    description="""This tool allows to get details on service identities. 
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
)
def report_run_service_identities_details(report_id: str, csv: bool = False, filter_expression: str = None):
    # This tool is generated using Britive SDK v4.3.0
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


@mcp.tool(
    name="report_run_user_secret_access",
    description="""This tool allows information on secret assigned to users. 
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
)
def report_run_user_secret_access(report_id: str, csv: bool = False, filter_expression: str = None):
    # This tool is generated using Britive SDK v4.3.0
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


@mcp.tool(
    name="report_run_secret_last_access",
    description="""This tool provides information on secrets and when they were accessed. 
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
)
def report_run_secret_last_access(report_id: str, csv: bool = False, filter_expression: str = None):
    # This tool is generated using Britive SDK v4.3.0
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


@mcp.tool(
    name="report_run_profiles_assigned_to_service_identities",
    description="""This tool provides information to get details on who has what access to profiles, applications and environments
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
)
def report_run_profiles_assigned_to_service_identities(
    report_id: str, csv: bool = False, filter_expression: str = None
):
    # This tool is generated using Britive SDK v4.3.0
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


@mcp.tool(
    name="report_run_profile_accessed_tags",
    description=""" This tool provides tags information associated with details on who has what access to applications, environments and profiles.
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
)
def report_run_profile_accessed_tags(report_id: str, csv: bool = False, filter_expression: str = None):
    # This tool is generated using Britive SDK v4.3.0
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


@mcp.tool(
    name="report_run_AI_identities_secret_last_access",
    description=""" This tool provides information on details of AI identities with secrets last access
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
)
def report_run_AI_identities_secret_last_access(report_id: str, csv: bool = False, filter_expression: str = None):
    # This tool is generated using Britive SDK v4.3.0
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


@mcp.tool(
    name="report_run_permission_details",
    description=""" This tool provides granular details on application permissions for specified application
                use this tool after application access tool to get more details on permissions and focus on permissionDefinition
        
        1. Use `reports_list` to find the report named 'Permission Details'.
        2. Extract its `reportId` and valid columns/operators.
        3. Call this tool with that `report_id` and optional filters. after the application access tool to have detailed permission information.

        Filterable columns include: `application`, `environment`,`permissionDefinition`,`scope`, `scopeType`, `name`,`applicationStatus`,`environmentStatus`,`type`, `highrisk`


        Examples:

        User may ask questions such as:
        -Show me what permissions are assigned to a role/policy in a `xyz` application
        -Show me which roles/policies in a `xyz` application have not been used in the past 30 days.


    Expected Response Format:
    Answer in a structured format (e.g., tables or bullet points).
    Include metadata like Application, Environment, account, permissions, permission description, status, etc., when relevant associated with application access. 
    Apply column-based filters precisely based on the question.

    Do not add any quotes around the values, even if they contain spaces or special characters. The tool will handle them correctly.
    Strictly use the operators defined in the `logs_operators` tool, such as `eq`, `sw`, `co`, etc. and if having negative context in filter matching then use operator `neq`, `nco` Do not use any other operators or formats.
    """,
)
def report_run_permission_details(report_id: str, csv: bool = False, filter_expression: str = None):
    # This tool is generated using Britive SDK v4.3.0
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


@mcp.tool(
    name="report_run_resource_historical_access",
    description=""" This tool provides information on resource checked out by users in last 90 days.
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
)
def report_run_resource_historical_access(report_id: str, csv: bool = False, filter_expression: str = None):
    # This tool is generated using Britive SDK v4.3.0
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


@mcp.tool(
    name="report_run_resource_last_access",
    description=""" This tool provides information on when a resource was used.
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
)
def report_run_resource_last_access(report_id: str, csv: bool = False, filter_expression: str = None):
    # This tool is generated using Britive SDK v4.3.0
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


@mcp.tool(
    name="report_run_resources_assigned_to_ai_identities",
    description=""" This tool provides information on resources assigned to ai identities.
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
)
def report_run_resources_assigned_to_ai_identities(report_id: str, csv: bool = False, filter_expression: str = None):
    # This tool is generated using Britive SDK v4.3.0
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


@mcp.tool(
    name="report_run_resources_assigned_to_all_identities",
    description=""" This tool provides information on resources assigned to all identities.
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
)
def report_run_resources_assigned_to_all_identities(report_id: str, csv: bool = False, filter_expression: str = None):
    # This tool is generated using Britive SDK v4.3.0
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


@mcp.tool(
    name="report_run_resources_assigned_to_service_identities",
    description=""" This tool provides information on resources assigned to service identities.
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
)
def report_run_resources_assigned_to_service_identities(
    report_id: str, csv: bool = False, filter_expression: str = None
):
    # This tool is generated using Britive SDK v4.3.0
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


@mcp.tool(
    name="report_run_resources_assigned_to_tags",
    description=""" This tool provides information on resources assigned to tags.
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
)
def report_run_resources_assigned_to_tags(report_id: str, csv: bool = False, filter_expression: str = None):
    # This tool is generated using Britive SDK v4.3.0
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


@mcp.tool(
    name="report_run_resources_assigned_to_users",
    description=""" This tool provides information on resources assigned to users.
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
)
def report_run_resources_assigned_to_users(report_id: str, csv: bool = False, filter_expression: str = None):
    # This tool is generated using Britive SDK v4.3.0
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


@mcp.tool(
    name="reports_list",
    description="""List all available reports and their metadata.
Use this tool to:
- Retrieve report names and their `reportId`s.
- Extract available filterable columns for each report.
- Understand which operators (e.g., `eq`, `co`, `gt`) are supported per column.

You must call this tool before using any `report_run_*` tool to ensure you have the correct `reportId`, column names, and operator support.
No parameters required.""",
)
def reports_list():
    # This tool is generated using Britive SDK v4.3.0
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
""",
)
def all_reports_run(report_id: str, csv: bool = False, filter_expression: str = None):
    # This tool is generated using Britive SDK v4.3.0
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


@mcp.tool(
    name="report_run_permission_details",
    description=""" This tool provides granular details on application permissions for specified application
                use this tool after application access tool to get more details on permissions and focus on permissionDefinition
        
        1. Use `reports_list` to find the report named 'Permission Details'.
        2. Extract its `reportId` and valid columns/operators.
        3. Call this tool with that `report_id` and optional filters. after the application access tool to have detailed permission information.

        Filterable columns include: `application`, `environment`,`permissionDefinition`,`scope`, `scopeType`, `name`,`applicationStatus`,`environmentStatus`,`type`, `highrisk`


        Examples:

        User may ask questions such as:
        -Show me what permissions are assigned to a role/policy in a `xyz` application
        -Show me which roles/policies in a `xyz` application have not been used in the past 30 days.


    Expected Response Format:
    Answer in a structured format (e.g., tables or bullet points).
    Include metadata like Application, Environment, account, permissions, permission description, status, etc., when relevant associated with application access. 
    Apply column-based filters precisely based on the question.

    Do not add any quotes around the values, even if they contain spaces or special characters. The tool will handle them correctly.
    Strictly use the operators defined in the `logs_operators` tool, such as `eq`, `sw`, `co`, etc. and if having negative context in filter matching then use operator `neq`, `nco` Do not use any other operators or formats.
    """,
)
def report_run_permission_details(report_id: str, csv: bool = False, filter_expression: str = None):
    # This tool is generated using Britive SDK v4.3.0
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
