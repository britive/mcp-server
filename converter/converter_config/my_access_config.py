from converter.converter_config.base import ToolConfig, ToolGroup

my_access_tools = ToolGroup(
    name="my_access",
    tools=[
        ToolConfig(
            function_name="checkout",
            ai_description="Use this tool when the user is denied access via MCP (e.g., 'access denied', 'not authorized') or implicitly indicates they can't access something they should. "
                "Also trigger if the user says 'need access', 'get access', or refers to Britive access. "
                "Prefer silent inference of 'profile_id' and 'environment_id' from prior context or conversation; ask only if unclear. "
                "Set 'programmatic=False' unless programmatic access is explicitly mentioned. "
                "Include 'justification' only if needed for approval (e.g., access typically restricted or user says 'need approval'). "
                "Use 'include_credentials=True' only if the user expects immediate use. "
                "When include_credentials=True and the response contains credentials.url, format the console link as a clickable markdown link instead of displaying the raw URL in a code block. Use format: [🔗 Click here to open console](url)"
                "Handle approval flows quietly, inform the user once if there's a delay, but avoid repeated updates unless asked. "
                "Accept optional 'ticket_id', 'ticket_type', or 'otp' if context provides them. "
                "Do not try to guess these parameters if not mentioned by the user or in the context. "
                "You can find the profile and environment IDs by using the `list_profiles` tool. "
                "If access was already granted, return it silently. "
                "If failure occurs (rejection, timeout, withdrawal), notify with minimal friction. "
                "Never use this tool when the user is only inquiring about existing access or wanting to check in access.",
            tool_name="my_access_checkout",
        ),
        ToolConfig(
            function_name="checkin",
            ai_description="Use this tool when the user has completed their task or explicitly indicates they no longer need access (e.g., 'done with access', 'you can check it in', 'I'm finished', or 'revoke access'). "
                "It is also appropriate to suggest check-in if the user asks what access they currently have and chooses to release it. "
                "If multiple profiles were checked out, ensure all are checked in, not just the most recent one. "
                "Prefer silent handling unless the user expects confirmation. The only required input is the 'transaction_id' of the profile that was previously checked out. "
                "If not already tracked or known from context, ask the user briefly. Do not invoke this tool preemptively unless the user's intent to end access is clear.",
        ),
        ToolConfig(
            function_name="list_profiles",
            ai_description="List all profiles available for checkout. "
                "This tool is useful for understanding what access options are available to the user. "
                "It can also be used to find the profile and environment IDs needed for the `checkout` tool. "
                "This tool does not require any parameters and will return a list of profiles with their details.",
        ),
        ToolConfig(
            function_name="whoami",
            ai_description="""
Use this tool to retrieve details of the currently authenticated identity (user or service). 
It returns information like username, type (user/service), and any other associated metadata.

When to Use:
- When the user asks questions like:
  - "Who am I?"
  - "What user is currently logged in?"
  - "Tell me about my account"
  - "What is my identity?"

- When the user refers to themselves using:
  - Words like "I", "me", "my", "mine"
  - Phrases that imply a self-reference (e.g., "my secrets", "my roles", "my entitlements")

- When another tool requires an identity as input, but the user did not specify one.
  - In such cases, use `whoami` first to fetch the identity, and then pass it to the next tool.

Constraints:
- Only use this tool when the user is referring to themselves.
- Do **not** use this tool when the user is asking about someone else.""",
        ),
    ]
)