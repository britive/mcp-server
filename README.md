# Britive MCP Server

Britive's MCP Server enables AI agents and users to interact with the Britive platform. Britive's MCP server exposes several tools that enable users and AI agents to interact with the Britive platform for dynamic access, query configurations, reporting, and access activity.

To learn more about MCPs, see [Get Started with MCP](https://modelcontextprotocol.io/docs/getting-started/intro).

---

## Prerequisites

- Python version 3.10 or higher. [Python downloads](https://www.python.org/downloads/).
- Any MCP client. For example: Claude Desktop, VS Code Copilot

---

## Installation

### Install with uv (Recommended)

```shell
uv pip install britive_mcp_server
```

### Install with pip

```shell
pip install britive_mcp_server
```

### Install from source

```shell
git clone https://github.com/britive/mcp-server.git
cd mcp-server
uv pip install -e .
```

---

## Usage

### Command Line Arguments

```shell
britive_mcp_server --tenant <your_tenant_name>
```

| Argument | Required | Description |
|----------|----------|-------------|
| `--tenant` | Yes | Britive tenant name (e.g., `my-company` for `my-company.britive.com`) |
| `--token` | No | Static API token (alternative to PyBritive CLI auth) |
| `--email` | No | Email for On-Behalf-Of (OBO) functionality |

All arguments can also be set via environment variables: `BRITIVE_TENANT`, `BRITIVE_STATIC_TOKEN`, `BRITIVE_EMAIL`.

---

## Configuring your MCP client

### Option 1: Using uvx (Recommended)

```json
{
  "mcpServers": {
    "britive": {
      "command": "uvx",
      "args": ["britive_mcp_server", "--tenant", "your_tenant_name"]
    }
  }
}
```

With static token:

```json
{
  "mcpServers": {
    "britive": {
      "command": "uvx",
      "args": [
        "britive_mcp_server",
        "--tenant", "your_tenant_name",
        "--token", "your_static_token"
      ]
    }
  }
}
```

### Option 2: Using installed command

```json
{
  "mcpServers": {
    "britive": {
      "command": "britive_mcp_server",
      "args": ["--tenant", "your_tenant_name"]
    }
  }
}
```

### Configuration file locations

- **Claude Desktop (Windows):** `%APPDATA%\Claude\claude_desktop_config.json`
- **Claude Desktop (macOS):** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **VS Code:** See [VS Code MCP documentation](https://code.visualstudio.com/docs/copilot/chat/mcp-servers)

---

## Authentication

### Option 1: PyBritive CLI (Recommended)

1. Install PyBritive CLI: [PyBritive Documentation](https://britive.github.io/python-cli/)

2. Configure and login:

   ```shell
   pybritive configure tenant
   pybritive login
   ```

### Option 2: Static Token

1. Generate a static token from Britive UI. See [API Tokens](https://docs.britive.com/v1/docs/api-tokens-1).

2. Pass via `--token` argument or `BRITIVE_STATIC_TOKEN` env var.

---

## On-Behalf-Of (OBO) Mode

For impersonating users, use the `--email` argument:

```json
{
  "mcpServers": {
    "britive": {
      "command": "uvx",
      "args": [
        "britive_mcp_server",
        "--tenant", "your_tenant_name",
        "--token", "your_service_identity_token",
        "--email", "user@example.com"
      ]
    }
  }
}
```

**Supported OBO tools:** `my_access`, `my_resources`, `my_secrets`

---

## Available Tools

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

```shell
# Install dev dependencies
uv sync

# Run tests
uv run pytest

# Format code
uv run black britive_mcp_tools
uv run ruff check britive_mcp_tools
```

---

## License

MIT
