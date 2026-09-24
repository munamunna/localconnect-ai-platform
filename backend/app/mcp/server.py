from mcp.server import MCPServer

from app.services.agent_availability_service import (
    check_freelancer_availability,
)
from app.services.agent_freelancer_service import search_freelancers


mcp = MCPServer("LocalConnect")


@mcp.tool()
def health_check() -> str:
    """Check whether the LocalConnect MCP server is running."""
    return "LocalConnect MCP server is healthy."


@mcp.tool()
def search_freelancers_tool(
    service: str,
    location: str,
):
    """Find verified and available LocalConnect freelancers by service and location."""
    return search_freelancers(
        service=service,
        location=location,
    )


@mcp.tool()
def check_availability_tool(
    service: str,
    location: str,
):
    """Check for verified and currently available freelancers by service and location."""
    return check_freelancer_availability(
        service=service,
        location=location,
    )