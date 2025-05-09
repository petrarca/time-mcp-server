"""Main module for the time-mcp-server."""

import sys

import click

from time_mcp_server.server import mcp


@click.command()
@click.option(
    "--port",
    type=int,
    default=8090,
    help="Port to run the server on (default: 8090)",
)
@click.option(
    "--transport",
    type=click.Choice(["stdio", "streamable-http"]),
    default="stdio",
    help="Transport to use for the server (default: stdio)",
)
def main(port: int, transport: str) -> None:
    """Run the time MCP server application."""
    # When using stdio transport, don't print anything to stdout/stderr
    if transport == "stdio":
        # Run the MCP server with stdio transport (default)
        mcp.run()
    else:
        # For HTTP transport, it's safe to print to stderr
        print(f"Starting Time MCP Server on port {port} with streamable-http transport...", file=sys.stderr)
        # Run the MCP server with streamable-http transport
        mcp.run(transport="streamable-http", host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()
