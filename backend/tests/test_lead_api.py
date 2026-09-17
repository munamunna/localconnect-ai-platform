from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_extract_lead_and_save_success():
    fake_lead = {
        "service": "electrician",
        "location": "Kozhikode",
        "urgency": "tomorrow",
        "problem": "wiring problem",
        "budget": None,
        "customer_intent": "service_request",
        "lead_priority": "high",
    }

    fake_saved_lead = (
        1,
        "electrician",
        "Kozhikode",
        "tomorrow",
        "wiring problem",
        None,
        "service_request",
        "high",
        "NEW",
        None,
    )

    from app.schemas.lead import LeadInformation

    lead = LeadInformation(**fake_lead)

    with patch(
        "app.main.extract_lead",
        return_value=lead,
    ) as mock_extract, patch(
        "app.main.save_lead",
        return_value=fake_saved_lead,
    ) as mock_save:

        response = client.post(
            "/api/leads/extract",
            json={
                "message": (
                    "I need an electrician in Kozhikode "
                    "tomorrow for a wiring problem."
                )
            },
        )

    assert response.status_code == 200

    data = response.json()

    assert data["lead_id"] == 1
    assert data["status"] == "NEW"
    assert data["lead"]["service"] == "electrician"
    assert data["lead"]["location"] == "Kozhikode"

    mock_extract.assert_called_once()
    mock_save.assert_called_once_with(lead)

def test_extract_lead_and_save_invalid_lead():
    from app.schemas.lead import LeadInformation

    lead = LeadInformation(
        service=None,
        location=None,
        urgency=None,
        problem=None,
        budget=None,
        customer_intent=None,
        lead_priority=None,
    )

    with patch(
        "app.main.extract_lead",
        return_value=lead,
    ), patch(
        "app.main.save_lead",
        side_effect=ValueError(
            "Cannot save lead without service or location"
        ),
    ):

        response = client.post(
            "/api/leads/extract",
            json={
                "message": "I need some help"
            },
        )

    assert response.status_code == 400

    assert response.json()["detail"] == (
        "Cannot save lead without service or location"
    )