from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_match_freelancers_success():
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
        "app.main.match_freelancers",
        return_value=fake_freelancers,
    ) as mock_service:

        response = client.post(
            "/api/freelancers/match",
            json={
                "service": "electrician",
                "location": "Kozhikode",
            },
        )

    assert response.status_code == 200

    data = response.json()

    assert "matches" in data
    assert len(data["matches"]) == 1

    freelancer = data["matches"][0]

    assert freelancer["id"] == 1
    assert freelancer["name"] == "Ahmed"
    assert freelancer["service"] == "electrician"
    assert freelancer["location"] == "Kozhikode"
    assert freelancer["phone"] == "9876543210"
    assert freelancer["verified"] is True
    assert freelancer["available"] is True

    mock_service.assert_called_once_with(
        service="electrician",
        location="Kozhikode",
    )


def test_match_freelancers_no_match():
    with patch(
        "app.main.match_freelancers",
        return_value=[],
    ):

        response = client.post(
            "/api/freelancers/match",
            json={
                "service": "plumber",
                "location": "Kozhikode",
            },
        )

    assert response.status_code == 200

    data = response.json()

    assert data["matches"] == []


def test_match_freelancers_missing_service():
    response = client.post(
        "/api/freelancers/match",
        json={
            "location": "Kozhikode",
        },
    )

    assert response.status_code == 422


def test_match_freelancers_missing_location():
    response = client.post(
        "/api/freelancers/match",
        json={
            "service": "electrician",
        },
    )

    assert response.status_code == 422

def test_register_freelancer_success():
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
        "app.main.register_freelancer",
        return_value=fake_freelancer,
    ) as mock_service:

        response = client.post(
            "/api/freelancers",
            json={
                "name": "Muhammed",
                "service": "plumber",
                "location": "Kozhikode",
                "phone": "9876500000",
            },
        )

    assert response.status_code == 201

    data = response.json()

    assert data["id"] == 2
    assert data["name"] == "Muhammed"
    assert data["service"] == "plumber"
    assert data["location"] == "Kozhikode"
    assert data["phone"] == "9876500000"
    assert data["verified"] is False
    assert data["available"] is True

    mock_service.assert_called_once_with(
        name="Muhammed",
        service="plumber",
        location="Kozhikode",
        phone="9876500000",
    )
def test_register_freelancer_missing_name():
    response = client.post(
        "/api/freelancers",
        json={
            "service": "plumber",
            "location": "Kozhikode",
            "phone": "9876500000",
        },
    )

    assert response.status_code == 422

def test_register_freelancer_missing_service():
    response = client.post(
        "/api/freelancers",
        json={
            "name": "Muhammed",
            "location": "Kozhikode",
            "phone": "9876500000",
        },
    )

    assert response.status_code == 422

def test_register_freelancer_missing_location():
    response = client.post(
        "/api/freelancers",
        json={
            "name": "Muhammed",
            "service": "plumber",
            "phone": "9876500000",
        },
    )

    assert response.status_code == 422

def test_register_freelancer_without_phone():
    fake_freelancer = (
        3,
        "Ahmed",
        "electrician",
        "Kozhikode",
        None,
        False,
        True,
        None,
    )

    with patch(
        "app.main.register_freelancer",
        return_value=fake_freelancer,
    ) as mock_service:

        response = client.post(
            "/api/freelancers",
            json={
                "name": "Ahmed",
                "service": "electrician",
                "location": "Kozhikode",
            },
        )

    assert response.status_code == 201

    data = response.json()

    assert data["id"] == 3
    assert data["name"] == "Ahmed"
    assert data["phone"] is None
    assert data["verified"] is False
    assert data["available"] is True

    mock_service.assert_called_once_with(
        name="Ahmed",
        service="electrician",
        location="Kozhikode",
        phone=None,
    )

from unittest.mock import patch


def test_verify_freelancer_success():
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
        "app.main.verify_freelancer_profile",
        return_value=fake_freelancer,
    ) as mock_service:
        response = client.post(
            "/api/freelancers/1/verify"
        )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == 1
    assert data["name"] == "Ahmed"
    assert data["service"] == "electrician"
    assert data["location"] == "Kozhikode"
    assert data["verified"] is True
    assert data["available"] is True

    mock_service.assert_called_once_with(1)


def test_verify_freelancer_invalid_id():
    with patch(
        "app.main.verify_freelancer_profile",
        side_effect=ValueError("Invalid freelancer ID"),
    ) as mock_service:
        response = client.post(
            "/api/freelancers/0/verify"
        )

    assert response.status_code == 400

    assert response.json()["detail"] == "Invalid freelancer ID"

    mock_service.assert_called_once_with(0)

def test_verify_freelancer_not_found():
    with patch(
        "app.main.verify_freelancer_profile",
        side_effect=ValueError("Freelancer not found"),
    ) as mock_service:
        response = client.post(
            "/api/freelancers/999/verify"
        )

    assert response.status_code == 400

    assert response.json()["detail"] == "Freelancer not found"

    mock_service.assert_called_once_with(999)