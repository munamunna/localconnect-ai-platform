import pytest

from app.mcp.server import mcp


@pytest.mark.anyio
async def test_health_check_tool_registered():
    tools = await mcp.list_tools()

    assert len(tools) == 1
    assert tools[0].name == "health_check"
    assert (
        tools[0].description
        == "Check whether the LocalConnect MCP server is running."
    )