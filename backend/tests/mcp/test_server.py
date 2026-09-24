import pytest

from app.mcp.server import mcp


@pytest.mark.anyio
async def test_mcp_tools_registered():
    tools = await mcp.list_tools()

    tool_names = [tool.name for tool in tools]

    assert "health_check" in tool_names
    assert "search_freelancers_tool" in tool_names