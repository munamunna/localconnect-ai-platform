from unittest.mock import patch

import pytest

from app.services.agent_freelancer_service import search_freelancers


def test_search_freelancers_success():
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
        "app.services.agent_freelancer_service.match_freelancers",
        return_value=expected,
    ) as mock_match:

        result = search_freelancers(
            service="Plumbing",
            location="Kozhikode",
        )

    assert result == expected

    mock_match.assert_called_once_with(
        service="plumbing",
        location="Kozhikode",
    )

def test_search_freelancers_strips_input():
    with patch(
        "app.services.agent_freelancer_service.match_freelancers",
        return_value=[],
    ) as mock_match:

        result = search_freelancers(
            service="  Plumbing  ",
            location="  Kozhikode  ",
        )

    assert result == []

    mock_match.assert_called_once_with(
        service="plumbing",
        location="Kozhikode",
    )


def test_search_freelancers_requires_service():
    with pytest.raises(
        ValueError,
        match="Service is required",
    ):
        search_freelancers(
            service="",
            location="Kozhikode",
        )


def test_search_freelancers_requires_location():
    with pytest.raises(
        ValueError,
        match="Location is required",
    ):
        search_freelancers(
            service="Plumbing",
            location="",
        )

def test_search_freelancers_normalizes_service():
    with patch(
        "app.services.agent_freelancer_service.match_freelancers",
        return_value=[],
    ) as mock_match:

        search_freelancers(
            service="web and app development",
            location="Payyoli",
        )

    mock_match.assert_called_once_with(
        service="web and app",
        location="Payyoli",
    )