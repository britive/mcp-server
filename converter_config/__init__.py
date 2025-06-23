from converter_config.system_prompt import SYSTEM_PROMPT

from converter_config. my_access_config import my_access_tools
from converter_config.audit_logs_logs_config import audit_logs_logs
from converter_config.reports_config import reports

TOOLS = {
    my_access_tools.name: my_access_tools.tools,
    audit_logs_logs.name: audit_logs_logs.tools,
    reports.name: reports.tools
}