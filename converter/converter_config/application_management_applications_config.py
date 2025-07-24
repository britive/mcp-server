from converter.converter_config.base import ToolConfig, ToolGroup

application_management_applications = ToolGroup(
    name="application_management.applications",
    tools=[
        ToolConfig(
            function_name="list",
            ai_description=(
                "Use this tool to retrieve a list of all applications available in the Britive tenant. "
                "This is typically the first step when identifying applications by name or filtering them "
                "based on user input. The results can be used to extract application IDs "
                "required for other tools."
            ),
            regenerate=True,
        ),
        ToolConfig(
            function_name="get",
            ai_description=(
                "Use this tool to fetch detailed information about a specific application using its application ID. "
                "This includes metadata such as the application's nativeId, which is essential for querying "
                "permissions or identity associations in other tools."
            ),
            regenerate=True,
        ),
    ]
)
