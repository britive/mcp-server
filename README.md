# Britive MCP Server

Britive's MCP Server enables AI agents and users to interact with the Britive platform. Britive's MCP server exposes several tools that enable users and AI agents to interact with the Britive platform for dynamic access, query configurations, reporting, and access activity.

To learn more about MCPs, see [Get Started with MCP](https://modelcontextprotocol.io/docs/getting-started/intro).

---

## Prerequisites

- Python version 3.10 or higher. [Python downloads](https://www.python.org/downloads/).
- Any MCP client. For example: Claude Desktop, VS Code Copilot

---

## Installation

### Option 1: Install with uv (Recommended)

```shell
uv pip install britive-mcp-tools
```

### Option 2: Install with pip

```shell
pip install britive-mcp-tools
```

### Option 3: Install from source

```shell
git clone https://github.com/britive/mcp-server.git
cd mcp-server
uv pip install -e .
```

---

## Configuring your MCP client

Authentication to the Britive platform can be performed using the Britive CLI or a Static Token.

### Option 1: CLI login using PyBritive (Recommended)

1. Install the PyBritive CLI if not installed. For more information, see [PyBritive Documentation](https://britive.github.io/python-cli/)

2. Configure the tenant:

   ```shell
   pybritive configure tenant
   ```

3. Log in to PyBritive:

   ```shell
   pybritive login
   ```

   For multiple tenants:

   ```shell
   pybritive login --tenant=<your_tenant_name>
   ```

4. Configure your MCP client (Claude Desktop, VS Code, etc.):

**Using uvx (recommended):**

```json
{
  "mcpServers": {
    "britive": {
      "command": "uvx",
      "args": ["britive-mcp-tools"],
      "env": {
        "BRITIVE_TENANT": "your_tenant_name"
      }
    }
  }
}
```

**Using britive-mcp command:**

```json
{
  "mcpServers": {
    "britive": {
      "command": "britive-mcp",
      "env": {
        "BRITIVE_TENANT": "your_tenant_name"
      }
    }
  }
}
```

### Option 2: Login using a static token

1. Generate a static token from Britive UI. For more information, see [API Tokens](https://docs.britive.com/v1/docs/api-tokens-1).

2. Configure your MCP client:

```json
{
  "mcpServers": {
    "britive": {
      "command": "britive-mcp",
      "env": {
        "BRITIVE_TENANT": "your_tenant_name",
        "BRITIVE_STATIC_TOKEN": "your_static_token_here"
      }
    }
  }
}
```

### Configuration file locations

- **Claude Desktop (Windows):** `%APPDATA%\Claude\claude_desktop_config.json`
- **Claude Desktop (macOS):** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **VS Code:** See [VS Code MCP documentation](https://code.visualstudio.com/docs/copilot/chat/mcp-servers)

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `BRITIVE_TENANT` | Yes | Your Britive tenant name (e.g., `my-company` for `my-company.britive.com`) |
| `BRITIVE_STATIC_TOKEN` | No | Static API token (alternative to PyBritive CLI auth) |
| `BRITIVE_EMAIL` | No | Email for On-Behalf-Of (OBO) functionality |

---

## Using On-Behalf-Of (OBO) Functionality

To use OBO MCP, set the `BRITIVE_EMAIL` environment variable to the email of the user you want to impersonate:

```json
{
  "mcpServers": {
    "britive": {
      "command": "britive-mcp",
      "env": {
        "BRITIVE_TENANT": "your_tenant_name",
        "BRITIVE_STATIC_TOKEN": "your_service_identity_token",
        "BRITIVE_EMAIL": "user@example.com"
      }
    }
  }
}
```

When `BRITIVE_EMAIL` is set, OBO mode takes priority. The `BRITIVE_STATIC_TOKEN` should be the token of the service identity performing impersonation.

**Supported OBO tools:**
- `my_access`
- `my_resources`
- `my_secrets`

---

## Available Tools

The MCP server exposes the following tool categories:

- **My Access** - Check out/check in privileged access
- **My Resources** - List and manage resources
- **My Secrets** - List and view secrets
- **Application Management** - List and manage applications
- **Audit Logs** - Query audit logs
- **Identity Management** - Manage users, service identities, and tags
- **Reports** - Run and retrieve reports
- **Security** - Manage active sessions

---

## Development

### Install development dependencies

```shell
uv pip install -e ".[dev]"
```

Or with uv sync:

```shell
uv sync
```

### Run tests

```shell
uv run pytest
```

### Code formatting

```shell
uv run black britive_mcp_tools
uv run ruff check britive_mcp_tools
```

---

## Connect to the MCP server

For more information, see [Connect to Local MCP Servers](https://modelcontextprotocol.io/quickstart/user).

---

## License

MIT
