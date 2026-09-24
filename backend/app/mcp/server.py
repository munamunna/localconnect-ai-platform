from mcp.server import MCPServer


mcp = MCPServer("LocalConnect")


@mcp.tool()
def health_check() -> str:
    """Check whether the LocalConnect MCP server is running."""
    return "LocalConnect MCP server is healthy."