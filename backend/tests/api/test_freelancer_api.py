from unittest.mock import patch


def test_register_freelancer_success(client):
    mock_freelancer = (
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
        "app.api.routes.freelancers.register_freelancer",
        return_value=mock_freelancer,
    ):
        response = client.post(
            "/api/freelancers",
            json={
                "name": "Rahul",
                "service": "Electrician",
                "location": "Kozhikode",
                "phone": "9999999999",
            },
        )

    assert response.status_code == 201

    data = response.json()

    assert data["id"] == 1
    assert data["name"] == "Rahul"
    assert data["service"] == "Electrician"
    assert data["location"] == "Kozhikode"
    assert data["phone"] == "9999999999"
    assert data["verified"] is False
    assert data["available"] is True


def test_register_freelancer_without_phone(client):
    mock_freelancer = (
        2,
        "Akhil",
        "Plumber",
        "Koyilandy",
        None,
        False,
        True,
        None,
    )

    with patch(
        "app.api.routes.freelancers.register_freelancer",
        return_value=mock_freelancer,
    ):
        response = client.post(
            "/api/freelancers",
            json={
                "name": "Akhil",
                "service": "Plumber",
                "location": "Koyilandy",
            },
        )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Akhil"
    assert data["phone"] is None


def test_register_freelancer_validation_error(client):
    with patch(
        "app.api.routes.freelancers.register_freelancer",
        side_effect=ValueError("Name is required"),
    ):
        response = client.post(
            "/api/freelancers",
            json={
                "name": "",
                "service": "Electrician",
                "location": "Kozhikode",
            },
        )

    assert response.status_code == 400
    assert response.json()["detail"] == "Name is required"


def test_match_freelancers_success(client):
    mock_matches = [
        (
            1,
            "Rahul",
            "Electrician",
            "Kozhikode",
            "9999999999",
            True,
            True,
            None,
        ),
        (
            2,
            "Akhil",
            "Electrician",
            "Kozhikode",
            "8888888888",
            True,
            True,
            None,
        ),
    ]

    with patch(
        "app.api.routes.freelancers.match_freelancers",
        return_value=mock_matches,
    ):
        response = client.post(
            "/api/freelancers/match",
            json={
                "service": "Electrician",
                "location": "Kozhikode",
            },
        )

    assert response.status_code == 200

    data = response.json()

    assert len(data["matches"]) == 2

    assert data["matches"][0]["name"] == "Rahul"
    assert data["matches"][0]["service"] == "Electrician"
    assert data["matches"][0]["location"] == "Kozhikode"

    assert data["matches"][1]["name"] == "Akhil"


def test_match_freelancers_validation_error(client):
    with patch(
        "app.api.routes.freelancers.match_freelancers",
        side_effect=ValueError("Service is required"),
    ):
        response = client.post(
            "/api/freelancers/match",
            json={
                "service": "",
                "location": "Kozhikode",
            },
        )

    assert response.status_code == 400
    assert response.json()["detail"] == "Service is required"


def test_verify_freelancer_success(client):
    mock_freelancer = (
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
        "app.api.routes.freelancers.verify_freelancer_profile",
        return_value=mock_freelancer,
    ):
        response = client.post(
            "/api/freelancers/1/verify"
        )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == 1
    assert data["verified"] is True


def test_verify_freelancer_not_found(client):
    with patch(
        "app.api.routes.freelancers.verify_freelancer_profile",
        side_effect=ValueError("Freelancer not found"),
    ):
        response = client.post(
            "/api/freelancers/999/verify"
        )

    assert response.status_code == 400
    assert response.json()["detail"] == "Freelancer not found"


def test_update_freelancer_availability_success(client):
    mock_freelancer = (
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
        "app.api.routes.freelancers.update_freelancer_availability_status",
        return_value=mock_freelancer,
    ):
        response = client.patch(
            "/api/freelancers/1/availability",
            json={
                "available": False,
            },
        )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == 1
    assert data["available"] is False