from unittest.mock import patch

import pytest

from app.services.agent_availability_service import (
    check_freelancer_availability,
)


def test_check_freelancer_availability():
    matches = [
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
        "app.services.agent_availability_service.search_freelancers",
        return_value=matches,
    ) as mock_search:

        result = check_freelancer_availability(
            service="electrician",
            location="Kozhikode",
        )

    assert result == matches

    mock_search.assert_called_once_with(
        service="electrician",
        location="Kozhikode",
    )


def test_check_freelancer_availability_returns_empty_list():
    with patch(
        "app.services.agent_availability_service.search_freelancers",
        return_value=[],
    ):

        result = check_freelancer_availability(
            service="electrician",
            location="Kozhikode",
        )

    assert result == []


def test_check_freelancer_availability_requires_service():
    with pytest.raises(
        ValueError,
        match="Service is required",
    ):
        check_freelancer_availability(
            service="",
            location="Kozhikode",
        )


def test_check_freelancer_availability_requires_location():
    with pytest.raises(
        ValueError,
        match="Location is required",
    ):
        check_freelancer_availability(
            service="electrician",
            location="",
        )