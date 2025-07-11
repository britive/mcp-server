from converter_config.system_prompt import SYSTEM_PROMPT

from converter_config. my_access_config import my_access_tools
from converter_config.audit_logs_logs_config import audit_logs_logs
from converter_config.reports_config import reports
from converter.converter_config.identity_service_config import identity_service_management
from converter.converter_config.identity_user_config import identity_user_management
from converter.converter_config.identity_tag_config import identity_tag_management
from converter.converter_config.security_config import security_active_session

TOOLS = {
    my_access_tools.name: my_access_tools.tools,
    audit_logs_logs.name: audit_logs_logs.tools,
    reports.name: reports.tools,
    identity_service_management.name: identity_service_management.tools,
    identity_user_management.name: identity_user_management.tools,
    identity_tag_management.name: identity_tag_management.tools,
    security_active_session.name: security_active_session.tools
}