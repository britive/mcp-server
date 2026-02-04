from mcp_init import mcp

# Both OBO MCP and non OBO MCP use my access
from ..tools.my_access import *
from ..tools.my_resources import *
from ..tools.my_secrets import *

if __name__ == "__main__":
    if not mcp.client.obo:
        # tools not supported by OBO

        from ..tools.application_management_applications import *
        from ..tools.audit_logs_logs import *
        from ..tools.identity_management_service_identities import *
        from ..tools.identity_management_tags import *
        from ..tools.identity_management_users import *
        from ..tools.reports import *
        from ..tools.security_active_sessions import *

    mcp.run()
    print("MCP server has started")
