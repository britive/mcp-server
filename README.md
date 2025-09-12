Britive's MCP Server enables AI agents and users to interact with the Britive platform. Britive's MCP server exposes several tools that enable users and AI agents to interact with the Britive platform for dynamic access, query configurations, reporting, and access activity.

To learn more about MCPs, see [Get Started with MCP](https://modelcontextprotocol.io/docs/getting-started/intro).

---

## Prerequisites

- Python version 3.10 or higher. Download from [Python downloads](https://www.python.org/downloads/).
- Ensure you have the latest version of Git installed and access to the repository. Download git from the [Git downloads](https://git-scm.com/downloads).
- Any MCP client. For example, Claude desktop and VS Code Copilot.

---

## Setting up the Britive MCP Server

1. Clone the GitHub repository that has the MCP server.

```shell
git clone https://github.com/britive/mcp-server.git
````

2. Change directory to `mcp-server`

```shell
cd mcp-server
```

3. Create a virtual environment:

```shell
python -m venv <virtual_env_name>
```

4. Activate the virtual environment:

* **Windows**

  ```shell
  <virtual_env_name>\Scripts\activate
  ```
* **macOS/Linux**

  ```shell
  source <virtual_env_name>/bin/activate
  ```

5. Install Python packages (dependencies)

    ```shell
    pip install -r requirements.txt
    ```

---

## Configuring your MCP client and Authentication
Authentication to the Britive platform can be performed using the Britive CLI or a Static Token:

* #### **Option 1: CLI login using PyBritive (Recommended):**

1. Install the PyBritive CLI if it is not already installed. For more information, see [PyBritive Documentation](https://britive.github.io/python-cli/)

2. Configure the tenant, if it has not already been configured, using the following command. To find out more about how to enter the tenant name, see [PyBritive: Tenant selection logic](https://britive.github.io/python-cli/#tenant-selection-logic).

    ```shell
    pybritive configure tenant
    ```

3. Log in to PyBritive:

   ```shell
   pybritive login
   ```

4. Log in using the following command if you have multiple tenants: 

   ```shell
   pybritive login --tenant=<your_tenant_name>
   ```
5. Log in directs you to the Britive login page, where you can enter your credentials.
6. Modify your MCP JSON file to configure the Britive MCP. The MCP JSON file may be located at different locations depending on your MCP client and how it was installed. 

    * Windows: If you are using the Claude desktop as your MCP client, the JSON file might be at this location: %APPDATA%\Claude\claude_desktop_config.json

      ```json
      {
        "servers": {
          "britive": {
            "command": "C:\\Users\\YourName\\mcp-server\\venv\\Scripts\\python.exe",
            "args": [
              "C:\\Users\\YourName\\mcp-server\\britive_mcp_tools\\core\\mcp_runner.py"
            ],
            "env": {
              "PYTHONPATH": "C:\\Users\\YourName\\mcp-server",
              "BRITIVE_TENANT": "your_tenant_name"
            }
          }
        }
      }
      ```
    * macOS/Linux: If you are using the Claude desktop on macOS as your MCP client, the JSON file might be at this location: ~/Library/Application Support/Claude/claude_desktop_config.json.
      ```json
      {
        "servers": {
          "britive": {
            "command": "/user/local/bin/python",
            "args": [
              "/Users/YourName/mcp-server/britive_mcp_tools/core/mcp_runner.py"
            ],
            "env": {
              "PYTHONPATH": "/Users/YourName/mcp-server",
              "BRITIVE_TENANT": "your_tenant_name",
            }
          }
        }
      }
      ```

Where:
<table>
  <tbody>
    <tr>
      <td><code>command</code></td>
      <td>Full path to the Python executable</td>
    </tr>
    <tr>
      <td><code>args</code></td>
      <td>Full path to the <code>britive_mcp_tools\core\mcp_runner.py</code></td>
    </tr>
    <tr>
      <td><code>PYTHONPATH</code></td>
      <td>Set the Python path to the <code>mcp-server</code> directory (repository)</td>
    </tr>
    <tr>
      <td><code>BRITIVE_TENANT</code></td>
      <td>Your tenant on Britive. This tenant name must match the name used in the PyBritive CLI</td>
    </tr>
  </tbody>
</table>

* #### **Option 2: Login using a static token:**

1. Generate a static token from the Britive UI. For more information, see [API Tokens](https://docs.britive.com/v1/docs/api-tokens-1).
2. Copy the token to use in the MCP JSON file.
3. Modify your MCP JSON file to configure the Britive MCP.  The MCP JSON file may be located at different locations depending on your MCP client and how it was installed.

    * Windows: If you are using the Claude desktop as your MCP client, the JSON file might be at this location: %APPDATA%\Claude\claude_desktop_config.json

      ```json
      {
        "servers": {
          "britive": {
            "command": "C:\\Users\\YourName\\mcp-server\\venv\\Scripts\\python.exe",
            "args": ["C:\\Users\\YourName\\mcp-server\\britive_mcp_tools\\core\\mcp_runner.py"
            ],
            "env": {
              "PYTHONPATH": "C:\\Users\\YourName\\mcp-server",
              "BRITIVE_TENANT": "your_tenant_name",
              "BRITIVE_STATIC_TOKEN": "your_static_token_here"
            }
          }
        }
      }
      ```
    * macOS/Linux: If you are using the Claude desktop on macOS as your MCP client, the JSON file might be at this location: ~/Library/Application Support/Claude/claude_desktop_config.json.
      ```json
      {
        "servers": {
          "britive": {
            "command": "/user/local/bin/python",
            "args": [
              "/Users/YourName/mcp-server/britive_mcp_tools/core/mcp_runner.py"
            ],
            "env": {
              "PYTHONPATH": "/Users/YourName/mcp-server",
              "BRITIVE_TENANT": "your_tenant_name",
              "BRITIVE_STATIC_TOKEN": "your_static_token_here"
            }
          }
        }
      }
      ```

**Where:**
<table>
  <tbody>
    <tr>
      <td><code>command</code></td>
      <td>Full path to the Python executable</td>
    </tr>
    <tr>
      <td><code>args</code></td>
      <td>Full path to the <code>britive_mcp_tools\core\mcp_runner.py</code> module.</td>
    </tr>
    <tr>
      <td><code>PYTHONPATH</code></td>
      <td>Set the Python path to the <code>mcp-server</code> directory (repository)</td>
    </tr>
    <tr>
      <td><code>BRITIVE_TENANT</code></td>
      <td>Your tenant on Britive. Do not use the entire FQDN for the subdomain. For example, for 
      <code>https://super-customer.test.aws.britive-corp.com</code>, use 
      <code>super-customer.test.aws</code> as a tenant subdomain.
      </td>
    </tr>
    <tr>
      <td><code>BRITIVE_STATIC_TOKEN</code></td>
      <td>Static token created in the previous step</td>
    </tr>
  </tbody>
</table>

 
## Connecting to the MCP server using a client application
For more information, see [Connect to Local MCP Servers](https://modelcontextprotocol.io/docs/develop/connect-local-servers).
