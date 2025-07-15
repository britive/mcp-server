from converter.converter_config.base import ToolConfig, ToolGroup

identity_user_management = ToolGroup(
    name="identity_management.users",
    tools=[
        ToolConfig(
            function_name="list",
            ai_description=(
                "Use this tool **only if the user has confirmed they are referring to user identities**. Do not assume the type of identity."
                "This tool lists all user identities available in the Britive platform with optional filters. "
                "It provides list of details such as userID, username, type, status, email, firstName, lastName. "
                "Use this tool to get userId based on filter options and use this id in further operations like enabling or disabling a service identity. "
                "You can filter the list by username, type, status, and tags to narrow down the results."
            ),         
            regenerate=True
            ),
        ToolConfig(
            function_name="get",
            ai_description=(
                "Use this tool **only if the user has confirmed they are referring to user identities**. Do not assume the type of identity."
                "This tool retrieves detailed information about a specific user identity by its userID. "
                "It provides comprehensive details including the identity's userId, username, email, firstName, lastName, type, status, created, modified, identityProvider and userTags. "
                "Use this tool to gather specific information about a user identity before taking actions like enabling or disabling it "
            ),         
            regenerate=True
            ),
        ToolConfig(
            function_name="search",
            ai_description=(
                "Use this tool **only if the user has confirmed they are referring to user identities**. Do not assume the type of identity."
                "This tool searches for user identities based on a query string. "
                "It allows you to find identities by name, username, firstName, lastName, email, type, status, identityProvider or other attributes. "
                "The search results include basic details such as userId, name, type, and status. "
                "Use this tool to quickly locate user identities that match specific criteria without needing to list all identities."
            ),         
            regenerate=True
            ),
        ToolConfig(
            function_name="enable",
            ai_description=(
                "Use this tool **only if the user has confirmed they are referring to user identities**. Do not assume the type of identity."
                "Checks the status of the specified user identity. If the status is inactive, prompts the user for confirmation to enable it. "
                "If confirmed, it performs the enable action. If the identity is already active, it informs the user and suggests disabling it instead."
            ),         
            regenerate=True
            ),
        ToolConfig(
            function_name="disable",
            ai_description=(
                "Use this tool **only if the user has confirmed they are referring to user identities**. Do not assume the type of identity."
                "Checks the status of the specified user identity. If the status is active, prompts the user for confirmation to disable it. "
                "If confirmed, it performs the disable action. If the identity is already inactive, it informs the user and suggests enabling it instead."
            ),
         regenerate=True
        )
    ]
)