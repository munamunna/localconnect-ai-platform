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