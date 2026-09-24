from unittest.mock import patch

import pytest

from app.mcp.server import check_availability_tool


def test_check_availability_tool_success():
    expected = [
        (
            1,
            "Ahmed",
            "electrical",
            "Kozhikode",
            "9876543210",
            True,
            True,
            None,
        )
    ]

    with patch(
        "app.mcp.server.check_freelancer_availability",
        return_value=expected,
    ) as mock_check:

        result = check_availability_tool(
            service="electrician",
            location="Kozhikode",
        )

    assert result == expected

    mock_check.assert_called_once_with(
        service="electrician",
        location="Kozhikode",
    )


def test_check_availability_tool_propagates_service_error():
    with patch(
        "app.mcp.server.check_freelancer_availability",
        side_effect=ValueError("Service is required"),
    ):

        with pytest.raises(
            ValueError,
            match="Service is required",
        ):
            check_availability_tool(
                service="",
                location="Kozhikode",
            )


def test_check_availability_tool_propagates_location_error():
    with patch(
        "app.mcp.server.check_freelancer_availability",
        side_effect=ValueError("Location is required"),
    ):

        with pytest.raises(
            ValueError,
            match="Location is required",
        ):
            check_availability_tool(
                service="electrician",
                location="",
            )