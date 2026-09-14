from unittest.mock import patch

import pytest

from app.services.freelancer_service import match_freelancers


def test_match_freelancers():
    fake_freelancers = [
        (
            1,
            "Ahmed",
            "electrician",
            "Kozhikode",
            "9876543210",
            True,
            True,
            None,
        )
    ]

    with patch(
        "app.services.freelancer_service.find_matching_freelancers",
        return_value=fake_freelancers,
    ) as mock_repository:

        result = match_freelancers(
            service="electrician",
            location="Kozhikode",
        )

    assert result == fake_freelancers

    mock_repository.assert_called_once_with(
        service="electrician",
        location="Kozhikode",
    )


def test_match_freelancers_requires_service():
    with pytest.raises(ValueError, match="Service is required"):
        match_freelancers(
            service="",
            location="Kozhikode",
        )


def test_match_freelancers_requires_location():
    with pytest.raises(ValueError, match="Location is required"):
        match_freelancers(
            service="electrician",
            location="",
        )

def test_match_freelancers_strips_input():
    with patch(
        "app.services.freelancer_service.find_matching_freelancers",
        return_value=[],
    ) as mock_repository:

        result = match_freelancers(
            service="  electrician  ",
            location="  Kozhikode  ",
        )

    assert result == []

    mock_repository.assert_called_once_with(
        service="electrician",
        location="Kozhikode",
    )