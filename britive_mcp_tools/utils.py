from __future__ import annotations
from typing import Any, Literal
from fastmcp import FastMCP
import os

from rich.align import Align
from rich.console import Console, Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text


LOGO_ASCII = r"""
██████╗   ██████╗   ██╗   ████████╗ ██╗ ██╗   ██╗ ███████╗
██╔══██╗  ██╔══██╗  ██║   ╚══██╔══╝ ██║ ██║   ██║ ██╔════╝
██████╔╝  ██████╔╝  ██║      ██║    ██║ ██║   ██║ █████╗  
██╔══██╗  ██╔══██╗  ██║      ██║    ██║  ██║ ██║  ██╔══╝  
██████╔╝  ██║  ██║  ██║      ██║    ██║  ╚╗██╔╝   ███████╗
╚═════╝   ╚═╝  ╚═╝  ╚═╝      ╚═╝    ╚═╝   ╚══╝    ╚══════╝
""".lstrip("\n")


def log_server_banner(
    server: FastMCP[Any],
    transport: Literal["stdio", "http", "sse", "streamable-http"],
    *,
    host: str | None = None,
    port: int | None = None,
    path: str | None = None,
) -> None:
    """Creates and logs a formatted banner with server information and logo.

    Args:
        transport: The transport protocol being used
        server_name: Optional server name to display
        host: Host address (for HTTP transports)
        port: Port number (for HTTP transports)
        path: Server path (for HTTP transports)
    """

    # Create the logo text
    logo_text = Text(LOGO_ASCII, style="bold green")

    # Create the main title
    title_text = Text("Britive MCP", style="bold blue")

    # Create the information table
    info_table = Table.grid(padding=(0, 1))
    info_table.add_column(style="bold", justify="center")  # Emoji column
    info_table.add_column(style="cyan", justify="left")  # Label column
    info_table.add_column(style="white", justify="left")  # Value column

    match transport:
        case "http" | "streamable-http":
            display_transport = "Streamable-HTTP"
        case "sse":
            display_transport = "SSE"
        case "stdio":
            display_transport = "STDIO"

    info_table.add_row("🖥️", "Server name:", server.name)
    info_table.add_row("📦", "Transport:", display_transport)

    # Show connection info based on transport
    if transport in ("http", "streamable-http", "sse"):
        if host and port:
            server_url = f"http://{host}:{port}"
            if path:
                server_url += f"/{path.lstrip('/')}"
            info_table.add_row("🔗", "Server URL:", server_url)

    # Add documentation link
    info_table.add_row("", "", "")
    info_table.add_row("📚", "Docs:", "https://docs.britive.com/shared/4442cfbe-ecd6-426b-827e-5cc1d339a652")

    # Create panel with logo, title, and information using Group
    panel_content = Group(
        Align.center(logo_text),
        Align.center(title_text),
        "",
        "",
        Align.center(info_table),
    )

    panel = Panel(
        panel_content,
        border_style="dim cyan",
        padding=(1, 4),
        expand=False,
    )

    console = Console(stderr=True)
    console.print(Group("\n", panel, "\n"))


def run_britive_mcp(
    mcp: FastMCP[Any],
    transport: Literal["stdio", "http", "sse", "streamable-http"],
    *,
    host: str | None = None,
    port: int | None = None,
    path: str | None = None,
) -> None:
    log_server_banner(mcp, transport, host=host, port=port, path=path)
    mcp.run(transport=transport, host=host, port=port, path=path, show_banner=False)


def get_env_or_raise(key: str) -> str:
    value = os.environ.get(key)
    if value is None or value.strip() == "":
        raise ValueError(
            f"\n\nMissing required environment variable: '{key}'. "
            f"Please define it in your .env file.\n"
        )
    return value