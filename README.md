# Britive MCP Server

Britive's MCP Server enables AI agents and users to interact with the Britive platform. Britive's MCP server exposes several tools that enable users and AI agents to interact with the Britive platform for dynamic access, query configurations, reporting, and access activity.

To learn more about MCPs, see [Get Started with MCP](https://modelcontextprotocol.io/docs/getting-started/intro).

---

## Prerequisites

- Python version 3.10 or higher. [Python downloads](https://www.python.org/downloads/).
- Any MCP client. For example: Claude Desktop, VS Code Copilot

---

---


### Command Line Arguments

```shell
britive_mcp_server --tenant <your_tenant_name>
```

| Argument | Required | Description |
|----------|----------|-------------|
| `--tenant` | Yes | Britive tenant name (e.g., `my-company` for `my-company.britive-app.com`) |
| `--token` | No | Static API token (alternative to PyBritive CLI auth) |
| `--email` | No | Email for On-Behalf-Of (OBO) functionality |

All arguments can also be set via environment variables: `BRITIVE_TENANT`, `BRITIVE_STATIC_TOKEN`, `BRITIVE_EMAIL`.

---

## Installing and configuring your MCP client

### Option 1: Using uvx (Recommended)

```json
{
  "mcpServers": {
    "britive": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/britive/mcp-server.git@feat/v1.0.0",
        "britive_mcp_server",
        "--tenant",
        "your_tenant_name",
      ]
    }
  },
  "preferences": {
    "coworkScheduledTasksEnabled": false,
    "sidebarMode": "chat"
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

## License

MIT
