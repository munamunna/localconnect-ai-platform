from unittest.mock import patch

from app.schemas.lead import LeadInformation


def test_extract_lead_success(client):
    mock_lead = LeadInformation(
        service="Electrician",
        location="Kozhikode",
        urgency="high",
        problem="Need wiring repair",
        budget="5000",
        customer_intent="hire_service",
        lead_priority="high",
    )

    mock_saved_lead = (
        1,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        "new",
    )

    with patch(
        "app.api.routes.leads.extract_lead",
        return_value=mock_lead,
    ), patch(
        "app.api.routes.leads.save_lead",
        return_value=mock_saved_lead,
    ):
        response = client.post(
            "/api/leads/extract",
            json={
                "message": (
                    "I need an electrician "
                    "in Kozhikode for wiring repair"
                )
            },
        )

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == (
        "I need an electrician "
        "in Kozhikode for wiring repair"
    )

    assert data["lead"]["service"] == "Electrician"
    assert data["lead"]["location"] == "Kozhikode"
    assert data["lead"]["urgency"] == "high"
    assert data["lead"]["problem"] == "Need wiring repair"
    assert data["lead"]["budget"] == "5000"
    assert data["lead"]["customer_intent"] == "hire_service"
    assert data["lead"]["lead_priority"] == "high"

    assert data["lead_id"] == 1
    assert data["status"] == "new"


def test_extract_lead_validation_error(client):
    with patch(
        "app.api.routes.leads.extract_lead",
        side_effect=ValueError("Message is required"),
    ):
        response = client.post(
            "/api/leads/extract",
            json={
                "message": "",
            },
        )

    assert response.status_code == 400
    assert response.json()["detail"] == "Message is required"


def test_extract_lead_server_error(client):
    with patch(
        "app.api.routes.leads.extract_lead",
        side_effect=Exception("LLM service failed"),
    ):
        response = client.post(
            "/api/leads/extract",
            json={
                "message": "I need an electrician",
            },
        )

    assert response.status_code == 500
    assert response.json()["detail"] == (
        "Lead extraction failed: LLM service failed"
    )


def test_match_lead_success(client):
    mock_lead = LeadInformation(
        service="Electrician",
        location="Kozhikode",
        urgency="high",
        problem="Need wiring repair",
        budget="5000",
        customer_intent="hire_service",
        lead_priority="high",
    )

    mock_freelancers = [
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
        "app.api.routes.leads.extract_lead",
        return_value=mock_lead,
    ), patch(
        "app.api.routes.leads.match_lead_to_freelancers",
        return_value=mock_freelancers,
    ):
        response = client.post(
            "/api/leads/match",
            json={
                "message": (
                    "I need an electrician "
                    "in Kozhikode"
                )
            },
        )

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == (
        "I need an electrician "
        "in Kozhikode"
    )

    assert data["lead"]["service"] == "Electrician"
    assert data["lead"]["location"] == "Kozhikode"
    assert data["lead"]["urgency"] == "high"

    assert len(data["matches"]) == 2

    assert data["matches"][0]["name"] == "Rahul"
    assert data["matches"][0]["service"] == "Electrician"
    assert data["matches"][0]["location"] == "Kozhikode"

    assert data["matches"][1]["name"] == "Akhil"


def test_match_lead_validation_error(client):
    with patch(
        "app.api.routes.leads.extract_lead",
        side_effect=ValueError("Message is required"),
    ):
        response = client.post(
            "/api/leads/match",
            json={
                "message": "",
            },
        )

    assert response.status_code == 400
    assert response.json()["detail"] == "Message is required"


def test_match_lead_server_error(client):
    mock_lead = LeadInformation(
        service="Electrician",
        location="Kozhikode",
    )

    with patch(
        "app.api.routes.leads.extract_lead",
        return_value=mock_lead,
    ), patch(
        "app.api.routes.leads.match_lead_to_freelancers",
        side_effect=Exception("Matching service failed"),
    ):
        response = client.post(
            "/api/leads/match",
            json={
                "message": "I need an electrician",
            },
        )

    assert response.status_code == 500
    assert response.json()["detail"] == (
        "Lead matching failed: Matching service failed"
    )