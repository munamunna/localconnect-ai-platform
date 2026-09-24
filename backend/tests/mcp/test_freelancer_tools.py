import pytest
from unittest.mock import patch

from app.mcp.server import search_freelancers_tool


def test_search_freelancers_tool_success():
    expected = [
        (
            1,
            "Ahmed",
            "Plumbing",
            "Kozhikode",
            "9876543210",
            True,
            True,
            None,
        )
    ]

    with patch(
        "app.mcp.server.search_freelancers",
        return_value=expected,
    ) as mock_search:

        result = search_freelancers_tool(
            service="Plumbing",
            location="Kozhikode",
        )

    assert result == expected

    mock_search.assert_called_once_with(
        service="Plumbing",
        location="Kozhikode",
    )


def test_search_freelancers_tool_propagates_service_error():
    with patch(
        "app.mcp.server.search_freelancers",
        side_effect=ValueError("Service is required"),
    ):

        with pytest.raises(
            ValueError,
            match="Service is required",
        ):
            search_freelancers_tool(
                service="",
                location="Kozhikode",
            )


def test_search_freelancers_tool_propagates_location_error():
    with patch(
        "app.mcp.server.search_freelancers",
        side_effect=ValueError("Location is required"),
    ):

        with pytest.raises(
            ValueError,
            match="Location is required",
        ):
            search_freelancers_tool(
                service="Plumbing",
                location="",
            )