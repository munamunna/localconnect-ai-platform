from unittest.mock import patch

import pytest

from app.services.freelancer_service import (
    match_freelancers,
    register_freelancer,
    verify_freelancer_profile,
)


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


def test_register_freelancer():
    fake_freelancer = (
        2,
        "Muhammed",
        "plumber",
        "Kozhikode",
        "9876500000",
        False,
        True,
        None,
    )

    with patch(
        "app.services.freelancer_service.create_freelancer",
        return_value=fake_freelancer,
    ) as mock_repository:

        result = register_freelancer(
            name="Muhammed",
            service="plumber",
            location="Kozhikode",
            phone="9876500000",
        )

    assert result == fake_freelancer

    mock_repository.assert_called_once_with(
        name="Muhammed",
        service="plumber",
        location="Kozhikode",
        phone="9876500000",
        verified=False,
        available=True,
    )

def test_register_freelancer_requires_name():
    with pytest.raises(ValueError, match="Name is required"):
        register_freelancer(
            name="",
            service="electrician",
            location="Kozhikode",
            phone="9876543210",
        )
def test_register_freelancer_requires_service():
    with pytest.raises(ValueError, match="Service is required"):
        register_freelancer(
            name="Ahmed",
            service="",
            location="Kozhikode",
            phone="9876543210",
        )
def test_register_freelancer_requires_location():
    with pytest.raises(ValueError, match="Location is required"):
        register_freelancer(
            name="Ahmed",
            service="electrician",
            location="",
            phone="9876543210",
        )

def test_register_freelancer_strips_input():
    fake_freelancer = (
        2,
        "Ahmed",
        "electrician",
        "Kozhikode",
        "9876543210",
        False,
        True,
        None,
    )

    with patch(
        "app.services.freelancer_service.create_freelancer",
        return_value=fake_freelancer,
    ) as mock_repository:

        result = register_freelancer(
            name="  Ahmed  ",
            service="  electrician  ",
            location="  Kozhikode  ",
            phone=" 9876543210 ",
        )

    assert result == fake_freelancer

    mock_repository.assert_called_once_with(
        name="Ahmed",
        service="electrician",
        location="Kozhikode",
        phone="9876543210",
        verified=False,
        available=True,
    )

from unittest.mock import patch


def test_verify_freelancer_profile():
    fake_freelancer = (
        1,
        "Ahmed",
        "electrician",
        "Kozhikode",
        "9876543210",
        True,
        True,
        None,
    )

    with patch(
        "app.services.freelancer_service.verify_freelancer",
        return_value=fake_freelancer,
    ) as mock_repository:
        result = verify_freelancer_profile(1)

    assert result == fake_freelancer
    mock_repository.assert_called_once_with(1)


def test_verify_freelancer_profile_rejects_invalid_id():
    with patch(
        "app.services.freelancer_service.verify_freelancer"
    ) as mock_repository:
        try:
            verify_freelancer_profile(0)
            assert False
        except ValueError as exc:
            assert str(exc) == "Invalid freelancer ID"

        mock_repository.assert_not_called()


def test_verify_freelancer_profile_freelancer_not_found():
    with patch(
        "app.services.freelancer_service.verify_freelancer",
        return_value=None,
    ) as mock_repository:
        try:
            verify_freelancer_profile(999)
            assert False
        except ValueError as exc:
            assert str(exc) == "Freelancer not found"

        mock_repository.assert_called_once_with(999)