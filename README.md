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
Authentication to the Britive platform can be performed using the Britive CLI, Static Token or oAuth :

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
              "BRITIVE_TENANT": "your_tenant_name",
              "AUTH_PROVIDER": "pybritive"
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
              "AUTH_PROVIDER": "pybritive"
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
    <tr>
      <td><code>AUTH_PROVIDER</code></td>
      <td>Since you chose PyBritive authentication, set <code>"AUTH_PROVIDER": "pybritve"</code></td>
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
              "BRITIVE_TENANT": "your_tenant_name",
              "BRITIVE_STATIC_TOKEN": "your_static_token_here",
              "AUTH_PROVIDER": "static_token"
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
              "BRITIVE_TENANT": "your_tenant_name",
              "BRITIVE_STATIC_TOKEN": "your_static_token_here",
              "AUTH_PROVIDER": "static_token"
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
    <tr>
      <td><code>AUTH_PROVIDER</code></td>
      <td>Since you chose static token authentication, set <code>"AUTH_PROVIDER": "static_token"</code></td>
    </tr>
  </tbody>
</table>


* #### **Option 3: OAuth Authentication**

  * Windows:

  1. Open **Command Prompt (cmd.exe)** or **PowerShell**.
  2. Set the environment variables:
     
      **Command Prompt (cmd.exe):**
      ```cmd
      set BRITIVE_TENANT=your_tenant_name
      set AUTH_PROVIDER=oauth
      ```

      **PowerShell:**

      ```powershell
      $env:BRITIVE_TENANT="your_tenant_name"
      $env:AUTH_PROVIDER="oauth"
      ```

  3. Run the MCP server:

      ```cmd
      python britive_mcp_tools\core\mcp_runner.py
      ```

    ---

  * Linux / macOS

  1. Open a terminal.

  2. Export the environment variables:

      ```bash
      export BRITIVE_TENANT=your_tenant_name
      export AUTH_PROVIDER=oauth
      ```

  3. Run the MCP server:

      ```bash
      python3 britive_mcp_tools/core/mcp_runner.py
      ```


**Where:**

<table>
  <tbody>
    <tr>
      <td><code>BRITIVE_TENANT</code></td>
      <td>Your Britive tenant name (must match your account’s tenant).</td>
    </tr>
    <tr>
      <td><code>AUTH_PROVIDER</code></td>
      <td>Since you chose oAuth authentication, set <code>"AUTH_PROVIDER": "oauth"</code>.</td>
    </tr>
  </tbody>
</table>

---

## Connecting to the MCP server using a client application

1. ####  If you are using **OAuth authentication**
    In your **MCP client settings** (e.g., Claude Desktop, MCP Inspector, etc.):

    * Change the **connection type** to **Streamable HTTP**.
    * Set the **MCP Server URL** to:

      ```bash
      http://127.0.0.1/
      ```

---

2. ####  If you are using **PyBritive** or **Static Token authentication**
    * The MCP server runs in **stdio mode** and can be connected directly by your MCP client.
    * For setup instructions, see:
       [Connect to Local MCP Servers](https://modelcontextprotocol.io/docs/develop/connect-local-servers)

---