# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with this repository.

## Project Overview

This is the Britive MCP (Model Context Protocol) Server - a Python package that enables AI agents to interact with the Britive privileged access management platform.

## Architecture

```
britive_mcp_tools/
├── __init__.py          # Package entry point, exposes main()
├── auth/
│   └── client_wrapper.py  # Britive client authentication (PyBritive CLI or static token)
├── core/
│   ├── mcp_init.py        # FastMCP server initialization, creates `mcp` instance
│   └── mcp_runner.py      # CLI entry point, loads tools and runs server
└── tools/                 # MCP tool implementations (each file auto-registers via @mcp.tool decorator)
    ├── my_access.py       # Checkout/checkin privileged access (supports OBO)
    ├── my_resources.py    # Resource management (supports OBO)
    ├── my_secrets.py      # Secret retrieval (supports OBO)
    ├── application_management_applications.py
    ├── audit_logs_logs.py
    ├── identity_management_*.py
    ├── reports.py
    └── security_active_sessions.py
```

## Key Concepts

- **FastMCP**: The server uses the `fastmcp` library. Tools are registered via `@mcp.tool()` decorators.
- **OBO (On-Behalf-Of)**: When `BRITIVE_EMAIL` env var is set, the server impersonates that user. Only `my_access`, `my_resources`, and `my_secrets` tools support OBO.
- **Authentication**: Either via PyBritive CLI (`pybritive login`) or static token (`BRITIVE_STATIC_TOKEN`).

## Common Commands

```bash
# Install in development mode
uv pip install -e .

# Install with dev dependencies
uv sync

# Run the MCP server
britive-mcp

# Run with uvx (no install needed)
uvx britive-mcp-tools

# Run tests
uv run pytest

# Format code
uv run black britive_mcp_tools
uv run ruff check britive_mcp_tools
```

## Environment Variables

- `BRITIVE_TENANT` (required): Tenant name (e.g., `my-company` for `my-company.britive.com`)
- `BRITIVE_STATIC_TOKEN` (optional): API token for authentication
- `BRITIVE_EMAIL` (optional): Email for OBO mode

## Adding New Tools

1. Create a new file in `britive_mcp_tools/tools/`
2. Import `mcp` from `..core.mcp_init`
3. Define functions with `@mcp.tool()` decorator
4. If the tool supports OBO, import it in `mcp_runner.py` at module level
5. If non-OBO only, add the module path to `_NON_OBO_MODULES` list in `mcp_runner.py`

## Package Configuration

The project uses `pyproject.toml` for all configuration:
- Build system: setuptools
- Version: Read dynamically from `britive_mcp_tools/__version__`
- Entry point: `britive-mcp` CLI command
