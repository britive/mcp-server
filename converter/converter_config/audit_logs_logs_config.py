from converter.converter_config.base import ToolConfig, ToolGroup

audit_logs_logs = ToolGroup(
    name="audit_logs.logs",
    tools=[
        ToolConfig(
            function_name="fields",
            ai_description="Call this before using query tool as it returns list of fields that can be used in a filter for an audit query.",
        ),
        ToolConfig(
            function_name="operators",
            ai_description="Call this before using query tool as it returns the list of operators that can be used in a filter for an audit query.",
        ),
        ToolConfig(
            function_name="query",
            ai_description="This is used to retrieve audit log events based on the fields and operators. You need to call the `fields` and `operators` tools before using this tool to ensure you have the correct fields and operators for your query.",
        )
    ]
)