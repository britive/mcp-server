# Britive MCP Tools - Quickstart Guide

This guide explains how to set up and use the generated MCP tools in this repository.

## 1. Clone the Repository

Clone this repository to your local machine:

```sh
git clone git@github.com:britive/mcp-server.git
cd mcp-server
```

## 2. Create Virtual Environement and Install Requirements

Create virtual environment
```sh
python -m venv <virtual_env_name>
```
Activate virtual environment

Windows
```sh
<virtual_env_name>\Scripts\activate
```
Linux

```sh
source <virtual_env_name>/Scripts/activate
```

Install the required Python packages in your created environment:

```sh
pip install -r requirements.txt
```

## 3. Login 
You have 2 options to authenticate:
1. **Pybritive CLI** : Authenticate with your Britive account using the [pybritive](https://pypi.org/project/pybritive/) CLI  

2. **Static Token** : Generated token on Britive's platform.
---
#### 1. **Pybritive CLI** 
Login with your Britive account using the [pybritive](https://pypi.org/project/pybritive/) CLI:

```sh
pybritive login
```
If you are having multiple tenant configured then use following command to login:

```sh
pybritive login --tenant=<tenant_name>
```

Follow the instructions to authenticate.

---
#### 2. **Static Token**
Generate a static token from Britive's platform, and then pass it in the configuration .json file. See details on how to use Static token in Section 4.5


## 4. Configure MCP JSON file

Sample json file

```json
{
  "servers": {
    "britive": {
      "command": "<path_to_the_repo>\\<virtual_env_name>\\Scripts\\python.exe",
      "args": [
        "<path_to_the_repo>\\mcp-server\\britive_mcp_tools\\core\\mcp_runner.py"
      ],
      "env": {
        "PYTHONPATH": "<path_to_the_repo>\\mcp-server",
        "BRITIVE_TENANT": "your_tenant",
        "BRITIVE_STATIC_TOKEN": "your_static_token",   
      }
    }
  }
}

```
---
| Line No | Key/Field        | Description                                                                |
| ------- | ---------------- | -------------------------------------------------------------------------- |
| 1       | `command`        | Full path to the Python executable inside the virtual environment.         |
| 2       | `args`           | Full path to the `britive_mcp_tools\core\mcp_runner.py` module.            |
| 3       | `PYTHONPATH`     | Set the Python path to `mcp-server` directory (repo).                      |
| 4       | `BRITIVE_TENANT` (Optional) | Your tenant on Britive. Default is `courage.dev2.aws`           |
| 5       | `BRITIVE_STATIC_TOKEN` (Optional) | Your Static token. Generate it from the Britive's platform |
---

## 5. Start the MCP Server

You can now start the MCP server using your configured environment.  
If using VS Code, you can launch the server via the MCP extension or by running:

```sh
python britive_mcp_tools/core/mcp_runner.py
```

Or use the `.vscode/mcp.json` configuration with your preferred MCP client.

---

## 6. Enable Copilot Agent Mode

Enable Copilot in Agent mode in your client (such as Claude Desktop or another MCP-compatible client).

## 7. Start Using MCP Tools

Begin with your prompt to test the MCP tools, for example:

> Show me my profile access.

or
> Show all active sessions.

---

For more details on available tools, see the source files in [`britive_mcp_tools/tools/`](britive_mcp_tools/tools/).

For more details on converter to generate tools [`Click here`](converter_readme.md)

---