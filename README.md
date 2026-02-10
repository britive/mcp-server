# Britive MCP Server

Britive's MCP Server enables AI agents and users to interact with the Britive platform. Britive's MCP server exposes several tools that enable users and AI agents to interact with the Britive platform for dynamic access, query configurations, reporting, and access activity.

To learn more about MCPs, see [Get Started with MCP](https://modelcontextprotocol.io/docs/getting-started/intro).

---

## Prerequisites

- Python version 3.10 or higher. [Python downloads](https://www.python.org/downloads/).
- Any MCP client. For example: Claude Desktop, VS Code Copilot

---

## Installing and Configuring the MCP Server

### Command Line Arguments

```shell
britive-mcp-server --tenant <your_tenant_name>
```

| Argument | Required | Description |
|----------|----------|-------------|
| `--tenant` | Yes | Britive tenant name (e.g., `my-company` for `my-company.britive-app.com`) |
| `--token` | No | Static API token (alternative to PyBritive CLI auth) |
| `--email` | No | Email for On-Behalf-Of (OBO) functionality |

All arguments can also be set via environment variables: `BRITIVE_TENANT`, `BRITIVE_STATIC_TOKEN`, `BRITIVE_EMAIL`.

### Installation Methods

There are two ways to run the MCP server:

- **`uvx` (no install required)** - Runs the package directly without installing it. Requires [uv](https://docs.astral.sh/uv/).
- **`pip install`** - Install the package, then use the `britive-mcp-server` command.

To install with pip:

```shell
pip install git+https://github.com/britive/mcp-server.git@feat/v1.0.0
```

### Authentication Methods

- **PyBritive CLI (Recommended)** - Authenticate via the PyBritive CLI. Install from [PyBritive Documentation](https://britive.github.io/python-cli/), then run `pybritive configure tenant` and `pybritive login`.
- **Static Token** - Generate a static API token from the Britive UI. See [API Tokens](https://docs.britive.com/v1/docs/api-tokens-1). Pass via `--token` argument.

### On-Behalf-Of (OBO) Mode

OBO mode allows the server to impersonate a specific user by passing their email via `--email`. This is useful when a service identity needs to perform actions on behalf of an end user.

**Supported OBO tools:** `my_access`, `my_resources`, `my_secrets`

---

### Example MCP Client Configurations

Below are example configurations for all combinations of installation method, authentication, and OBO mode.

#### uvx + PyBritive CLI Auth

```json
{
  "mcpServers": {
    "britive": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/britive/mcp-server.git@feat/v1.0.0",
        "britive-mcp-server",
        "--tenant", "your_tenant_name"
      ]
    }
  }
}
```

#### uvx + PyBritive CLI Auth + OBO

```json
{
  "mcpServers": {
    "britive": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/britive/mcp-server.git@feat/v1.0.0",
        "britive-mcp-server",
        "--tenant", "your_tenant_name",
        "--email", "user@example.com"
      ]
    }
  }
}
```

#### uvx + Static Token Auth

```json
{
  "mcpServers": {
    "britive": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/britive/mcp-server.git@feat/v1.0.0",
        "britive-mcp-server",
        "--tenant", "your_tenant_name",
        "--token", "your_static_token"
      ]
    }
  }
}
```

#### uvx + Static Token Auth + OBO

```json
{
  "mcpServers": {
    "britive": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/britive/mcp-server.git@feat/v1.0.0",
        "britive-mcp-server",
        "--tenant", "your_tenant_name",
        "--token", "your_static_token",
        "--email", "user@example.com"
      ]
    }
  }
}
```

#### pip install + PyBritive CLI Auth

```json
{
  "mcpServers": {
    "britive": {
      "command": "britive-mcp-server",
      "args": [
        "--tenant", "your_tenant_name"
      ]
    }
  }
}
```

#### pip install + PyBritive CLI Auth + OBO

```json
{
  "mcpServers": {
    "britive": {
      "command": "britive-mcp-server",
      "args": [
        "--tenant", "your_tenant_name",
        "--email", "user@example.com"
      ]
    }
  }
}
```

#### pip install + Static Token Auth

```json
{
  "mcpServers": {
    "britive": {
      "command": "britive-mcp-server",
      "args": [
        "--tenant", "your_tenant_name",
        "--token", "your_static_token"
      ]
    }
  }
}
```

#### pip install + Static Token Auth + OBO

```json
{
  "mcpServers": {
    "britive": {
      "command": "britive-mcp-server",
      "args": [
        "--tenant", "your_tenant_name",
        "--token", "your_static_token",
        "--email", "user@example.com"
      ]
    }
  }
}
```

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
