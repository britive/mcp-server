import os
from configparser import ConfigParser
from fastmcp import FastMCP
from britive.britive import Britive
from dotenv import load_dotenv
from britive.exceptions import UnauthorizedRequest
import datetime
from typing import Optional

load_dotenv()


def britive_client(tenant: str = "") -> Britive | None:
    tenant = tenant if tenant else os.getenv("BRITIVE_TENANT", "courage.dev2.aws")
    tenant_config = ConfigParser()
    tenant_config.read(os.path.expanduser("~/.britive/pybritive.config"))
    tenant_dns = tenant_config[f"tenant-{tenant}"]["name"]
    token_config = ConfigParser()
    token_config.read(os.path.expanduser("~/.britive/pybritive.credentials"))
    token = token_config[tenant]["accessToken"]
    try:
        return Britive(tenant=tenant_dns, token=token)
    except UnauthorizedRequest as uae:
        print(str(uae).rsplit("-", maxsplit=1)[-1].strip()) 

mcp = FastMCP(name="Britive Tool Server", instruction="""
You are a secure and intelligent assistant integrated with Britive and MCP. Your primary goal is to help the user accomplish tasks.
You have access to various tools that allow you to interact with Britive's API, manage access, and retrieve information.

-> When to use checkout tool?
    Whenever you encounter access-related failures (e.g., 'access denied', 'unauthorized', 'permission required'), whether explicitly in responses or implied by the user's request, consider invoking the Britive access checkout tool. Use contextual understanding to determine when the user might need access, even if they don't ask directly. Minimize interruptions by inferring parameters from prior context when possible. Only prompt the user if essential inputs are unclear. 

-> How to use the reports tool?
    To run any report:
    1. Start by using the `reports_list` tool to retrieve the report ID by matching its name.
    2. View the available columns along with their supported operators that you can use for filtering in each report.
    3. Use the appropriate `report_run_*` tool with the `report_id` and optional filters.

    Note on filters:
    - Use the exact column names and only supported operators (like `eq`, `co`, `sw`).
    - Format filters as: `columnName operator value`. E.g., `profile eq admin`
    - Combine filters using `and`. E.g., `profile eq admin and application co aws`
    - **Do not use quotes** around values, even with spaces or special characters.

    Filter fallback logic:
    If a report query using `eq` (equals) operator returns no data, retry the same query using `co` (contains) operator for better matching, but only if `co` is a supported operator for that column.
    For example:
    - If `name eq John` returns no results and `name` supports `co`, retry with `name co John`.
    Ensure fallback only happens when no results are returned and the `co` operator is supported for that column, as per metadata returned from `reports_list`.
""")
britive = britive_client()

audit_logs_logs = britive.audit_logs.logs
my_access = britive.my_access
reports = britive.reports

