import importlib

from .mcp_init import mcp

# Both OBO MCP and non OBO MCP use these tools
from ..tools import my_access
from ..tools import my_resources
from ..tools import my_secrets

# Non-OBO tool modules
_NON_OBO_MODULES = [
    "britive_mcp_tools.tools.application_management_applications",
    "britive_mcp_tools.tools.audit_logs_logs",
    "britive_mcp_tools.tools.identity_management_service_identities",
    "britive_mcp_tools.tools.identity_management_tags",
    "britive_mcp_tools.tools.identity_management_users",
    "britive_mcp_tools.tools.reports",
    "britive_mcp_tools.tools.security_active_sessions",
]


def run():
    """Run the Britive MCP server."""
    if not mcp.client.obo:
        # Load tools not supported by OBO
        for module_name in _NON_OBO_MODULES:
            importlib.import_module(module_name)

    mcp.run()


if __name__ == "__main__":
    from britive_mcp_tools import main
    main()
