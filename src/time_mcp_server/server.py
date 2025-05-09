"""Time MCP Server implementation using FastMCP."""

from fastmcp import FastMCP  # noqa: I001

from time_mcp_server.tools import get_current_time, get_time_components

# Create a FastMCP server instance
mcp = FastMCP(name="TimeMCPServer")

# Register the tools with the MCP server
mcp.tool()(get_current_time)
mcp.tool()(get_time_components)
