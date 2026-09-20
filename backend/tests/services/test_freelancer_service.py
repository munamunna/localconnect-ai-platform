from unittest.mock import patch

import pytest

from app.services.freelancer_service import (
    match_freelancers,
    register_freelancer,
    verify_freelancer_profile,
    update_freelancer_availability_status,
)


def test_match_freelancers_success():
    expected = [
        (
            1,
            "Rahul",
            "Electrician",
            "Kozhikode",
            "9999999999",
            True,
            True,
            None,
        )
    ]

    with patch(
        "app.services.freelancer_service.find_matching_freelancers",
        return_value=expected,
    ) as mock_repository:

        result = match_freelancers(
            service=" Electrician ",
            location=" Kozhikode ",
        )

    assert result == expected

    mock_repository.assert_called_once_with(
        service="Electrician",
        location="Kozhikode",
    )


def test_match_freelancers_missing_service():
    with pytest.raises(
        ValueError,
        match="Service is required",
    ):
        match_freelancers(
            service="",
            location="Kozhikode",
        )


def test_match_freelancers_missing_location():
    with pytest.raises(
        ValueError,
        match="Location is required",
    ):
        match_freelancers(
            service="Electrician",
            location="",
        )


def test_register_freelancer_success():
    expected = (
        1,
        "Rahul",
        "Electrician",
        "Kozhikode",
        "9999999999",
        False,
        True,
        None,
    )

    with patch(
        "app.services.freelancer_service.create_freelancer",
        return_value=expected,
    ) as mock_repository:

        result = register_freelancer(
            name=" Rahul ",
            service=" Electrician ",
            location=" Kozhikode ",
            phone=" 9999999999 ",
        )

    assert result == expected

    mock_repository.assert_called_once_with(
        name="Rahul",
        service="Electrician",
        location="Kozhikode",
        phone="9999999999",
        verified=False,
        available=True,
    )


def test_register_freelancer_without_phone():
    expected = (
        1,
        "Rahul",
        "Electrician",
        "Kozhikode",
        None,
        False,
        True,
        None,
    )

    with patch(
        "app.services.freelancer_service.create_freelancer",
        return_value=expected,
    ) as mock_repository:

        result = register_freelancer(
            name="Rahul",
            service="Electrician",
            location="Kozhikode",
        )

    assert result == expected

    mock_repository.assert_called_once_with(
        name="Rahul",
        service="Electrician",
        location="Kozhikode",
        phone=None,
        verified=False,
        available=True,
    )


def test_register_freelancer_invalid_name():
    with pytest.raises(
        ValueError,
        match="Name is required",
    ):
        register_freelancer(
            name="",
            service="Electrician",
            location="Kozhikode",
        )


def test_register_freelancer_invalid_service():
    with pytest.raises(
        ValueError,
        match="Service is required",
    ):
        register_freelancer(
            name="Rahul",
            service="",
            location="Kozhikode",
        )


def test_register_freelancer_invalid_location():
    with pytest.raises(
        ValueError,
        match="Location is required",
    ):
        register_freelancer(
            name="Rahul",
            service="Electrician",
            location="",
        )


def test_verify_freelancer_success():
    expected = (
        1,
        "Rahul",
        "Electrician",
        "Kozhikode",
        "9999999999",
        True,
        True,
        None,
    )

    with patch(
        "app.services.freelancer_service.verify_freelancer",
        return_value=expected,
    ) as mock_repository:

        result = verify_freelancer_profile(1)

    assert result == expected

    mock_repository.assert_called_once_with(1)


def test_verify_freelancer_invalid_id():
    with pytest.raises(
        ValueError,
        match="Invalid freelancer ID",
    ):
        verify_freelancer_profile(0)


def test_verify_freelancer_not_found():
    with patch(
        "app.services.freelancer_service.verify_freelancer",
        return_value=None,
    ):
        with pytest.raises(
            ValueError,
            match="Freelancer not found",
        ):
            verify_freelancer_profile(999)


def test_update_freelancer_availability_success():
    expected = (
        1,
        "Rahul",
        "Electrician",
        "Kozhikode",
        "9999999999",
        True,
        False,
        None,
    )

    with patch(
        "app.services.freelancer_service.update_freelancer_availability",
        return_value=expected,
    ) as mock_repository:

        result = update_freelancer_availability_status(
            freelancer_id=1,
            available=False,
        )

    assert result == expected

    mock_repository.assert_called_once_with(
        freelancer_id=1,
        available=False,
    )


def test_update_freelancer_availability_invalid_id():
    with pytest.raises(
        ValueError,
        match="Invalid freelancer ID",
    ):
        update_freelancer_availability_status(
            freelancer_id=0,
            available=False,
        )


def test_update_freelancer_availability_not_found():
    with patch(
        "app.services.freelancer_service.update_freelancer_availability",
        return_value=None,
    ):
        with pytest.raises(
            ValueError,
            match="Freelancer not found",
        ):
            update_freelancer_availability_status(
                freelancer_id=999,
                available=False,
            )