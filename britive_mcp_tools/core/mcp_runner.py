import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from britive_mcp_tools.core.mcp_init import mcp

# Both OBO MCP and non OBO MCP use my access
from britive_mcp_tools.tools.my_access import *

if __name__ == "__main__":
    if not mcp.client.obo:
        # tools not supported by OBO

        from britive_mcp_tools.tools.application_management_applications import *
        from britive_mcp_tools.tools.audit_logs_logs import *
        from britive_mcp_tools.tools.identity_management_service_identities import *
        from britive_mcp_tools.tools.identity_management_tags import *
        from britive_mcp_tools.tools.identity_management_users import *
        from britive_mcp_tools.tools.my_resources import *
        from britive_mcp_tools.tools.my_secrets import *
        from britive_mcp_tools.tools.reports import *
        from britive_mcp_tools.tools.security_active_sessions import *

    mcp.run()
