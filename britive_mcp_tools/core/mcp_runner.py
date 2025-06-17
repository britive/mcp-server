import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from britive_mcp_tools.core.mcp_init import mcp
from britive_mcp_tools.tools.my_access import *
from britive_mcp_tools.tools.audit_logs_logs import *
from britive_mcp_tools.tools.reports import *
from britive_mcp_tools.tools.identity_management_service_identities import *
from britive_mcp_tools.tools.identity_management_users import *
from britive_mcp_tools.tools.identity_management_tags import *
from britive_mcp_tools.tools.security_active_sessions import *
from britive_mcp_tools.tools.application_management_applications import *

if __name__ == '__main__':
    mcp.run()
