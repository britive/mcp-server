__version__ = "1.0.0"


def main():
    """Entry point for the Britive MCP server."""
    from .core.mcp_runner import main as _main
    _main()


__all__ = ["__version__", "main"]
