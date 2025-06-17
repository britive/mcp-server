**User Guide: Britive MCP Tool Generator**

---

**Purpose:**
This guide helps users understand how to use the Britive MCP Tool Generator to automatically generate or update tool functions based on the SDK and a modular config file structure.

---

**Step-by-Step Guide:**

**Step 1: Setup Environment**

* Clone the project repository.
* Install dependencies:

  ```bash
  pip install -r requirements.txt
  ```
* Add necessary environment variables in a `.env` file (BRITIVE_API_TOKEN, BRITIVE_TENANT).

**Step 2: Define Tool Configuration (Per Controller)**

* Create a separate config file for each controller using `ToolGroup` and `ToolConfig` in the `converter_config` directory :

```python
# audit_logs_logs.py

from converter_config.base import ToolConfig, ToolGroup

audit_logs_logs = ToolGroup(
    name="audit_logs.logs",
    tools=[
        ToolConfig(
            function_name="fields",
            ai_description="Return list of fields that can be used in a filter for an audit query."
        ),
        ToolConfig(
            function_name="operators",
            ai_description="Return the list of operators that can be used in a filter for an audit query."
        ),
        ToolConfig(
            function_name="query",
            ai_description="Retrieve audit log events."
        )
    ]
)
```

**Step 3: Register Config in Central File**

* Add the controller config to `converter_config/__init__.py`:

```python
from converter_config.system_prompt import SYSTEM_PROMPT
from converter_config.my_access_config import my_access_tools
from converter_config.audit_logs_logs_config import audit_logs_logs

TOOLS = {
    my_access_tools.name: my_access_tools.tools,
    audit_logs_logs.name: audit_logs_logs.tools,
#   your_controller.name: your_controller.tools
}
```

**Step 4: Run the Tool Generator Script**

* Update the MCP tools (Provide the already existing directory path of generated MCP Tools):

```bash
python3 converter.py --output britive_tools_mcp
```

* To generate all tools from scratch (Provide new directory path to avoid overwritting existing tools):

```bash
python3 converter.py --output britive_tools_mcp.py --all
```

---

**How It Works:**

* Loads the modular config and identifies each controller.
* Uses Python reflection to get all available SDK methods.
* Filters and selects methods based on the config.
* Generates or updates tool functions.

---

**Common Scenarios:**

* **Add a new method**

  * Add the method to the class-specific config file.
  * Rerun the script with `--output` flag and give the directory path for tools which you want to update.

* **Update an existing method**

  * Add `regenerate=True` in the `ToolConfig`.
  * Rerun the script.

* **Regenerate all tools from scratch**

  * Run the script with `--all` flag.

---

**Troubleshooting:**

* **Tool not generated?** Ensure the method exists in the SDK and matches the config.
* **Syntax issues?** Check function parameter names and types.

---

**Best Practices:**

* Write clear `ai_description` and examples for better LLM results.
* Avoid manual edits to the generated file.
