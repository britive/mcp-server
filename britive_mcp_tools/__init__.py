__version__ = "1.0.0"

import argparse
import os


def main():
    """Entry point for the Britive MCP server."""
    parser = argparse.ArgumentParser(description="Britive MCP Server")
    parser.add_argument(
        "--tenant",
        type=str,
        default=os.getenv("BRITIVE_TENANT"),
        help="Britive tenant name (e.g., 'my-company' for my-company.britive.com)",
    )
    parser.add_argument(
        "--token",
        type=str,
        default=os.getenv("BRITIVE_STATIC_TOKEN"),
        help="Static API token for authentication (alternative to PyBritive CLI)",
    )
    parser.add_argument(
        "--email",
        type=str,
        default=os.getenv("BRITIVE_EMAIL"),
        help="Email for On-Behalf-Of (OBO) functionality",
    )

    args = parser.parse_args()

    if not args.tenant:
        parser.error("--tenant is required (or set BRITIVE_TENANT env var)")

    # Set env vars for downstream code
    os.environ["BRITIVE_TENANT"] = args.tenant
    if args.token:
        os.environ["BRITIVE_STATIC_TOKEN"] = args.token
    if args.email:
        os.environ["BRITIVE_EMAIL"] = args.email

    from .core.mcp_runner import main as _main
    _main()


__all__ = ["__version__", "main"]
