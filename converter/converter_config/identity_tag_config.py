from converter_config.base import ToolConfig, ToolGroup

identity_tag_management = ToolGroup(
    name="identity_management.tags",
    tools=[
        ToolConfig(
            function_name="list",
            ai_description="This tool lists all tag identities available in the Britive platform. It provides list of details such as tagId, name, type, and status. Use this tool to get tagId based on filter options and use this id in further operations like enabling or disabling a tag identity. You can filter the list by name, type, status, and tags to narrow down the results.",         
            regenerate=True
            ),
        ToolConfig(
            function_name="get",
            ai_description="This tool retrieves detailed information about a specific tag identity by its tagID. It provides comprehensive details including the identity's name, type, status, created date, modified date, last login, token expires on, token expiration in days, type of serviceIdentity type and any associated tags. Use this tool to gather specific information about a service identity before taking actions like enabling or disabling it ",         
            regenerate=True
            ),
        ToolConfig(
            function_name="search",
            ai_description="This tool searches for tag identities based on a query string. It allows you to find identities by name, type, or other attributes. The search results include basic details such as identity ID, name, type, and status. Use this tool to quickly locate tag identities that match specific criteria without needing to list all identities.",         
            regenerate=True
            ),
        ToolConfig(
            function_name="enable",
            ai_description="Checks the status of the specified tag identity. If the status is inactive, prompts the user for confirmation to enable it. If confirmed, it performs the enable action. If the identity is already active, it informs the user and suggests disabling it instead.",         
            regenerate=True
            ),
        ToolConfig(
            function_name="disable",
            ai_description="Checks the status of the specified tag identity. If the status is active, prompts the user for confirmation to disable it. If confirmed, it performs the disable action. If the identity is already inactive, it informs the user and suggests enabling it instead.",
         regenerate=True
        )
    ]
)