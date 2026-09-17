from unittest.mock import MagicMock, patch
from app.schemas.lead import LeadInformation
from app.services.lead_service import (
    extract_lead,
    save_lead,
)
import pytest
from pydantic import ValidationError


def test_extract_lead():

    fake_response = MagicMock()

    fake_response.message.content = """
    {
        "service": "electrician",
        "location": "Kozhikode",
        "urgency": "tomorrow",
        "problem": "wiring problem",
        "budget": null,
        "customer_intent": "service request",
        "lead_priority": "high"
    }
    """

    with patch(
        "app.llm.ollama_llm.chat",
        return_value=fake_response,
    ):

        lead = extract_lead(
            "I need an electrician in Kozhikode tomorrow. There is a wiring problem in my house."
        )

    assert lead.service == "electrician"
    assert lead.location == "Kozhikode"
    assert lead.urgency == "tomorrow"
    assert lead.problem == "wiring problem"
    assert lead.budget is None
    assert lead.customer_intent == "service request"
    assert lead.lead_priority == "high"

def test_extract_lead_with_missing_information():

    fake_response = MagicMock()

    fake_response.message.content = """
    {
        "service": "electrician",
        "location": null,
        "urgency": null,
        "problem": null,
        "budget": null,
        "customer_intent": "service request",
        "lead_priority": "medium"
    }
    """

    with patch(
        "app.llm.ollama_llm.chat",
        return_value=fake_response,
    ):

        lead = extract_lead(
            "I need an electrician."
        )

    assert lead.service == "electrician"
    assert lead.location is None
    assert lead.urgency is None
    assert lead.problem is None
    assert lead.budget is None

def test_extract_plumber_lead():

    fake_response = MagicMock()

    fake_response.message.content = """
    {
        "service": "plumber",
        "location": "Dubai",
        "urgency": null,
        "problem": "water leakage",
        "budget": null,
        "customer_intent": "service request",
        "lead_priority": "medium"
    }
    """

    with patch(
        "app.llm.ollama_llm.chat",
        return_value=fake_response,
    ):

        lead = extract_lead(
            "I need a plumber in Dubai. There is a water leakage."
        )

    assert lead.service == "plumber"
    assert lead.location == "Dubai"
    assert lead.problem == "water leakage"    

def test_extract_lead_with_invalid_output():

    fake_response = MagicMock()

    fake_response.message.content = """
    {
        "service": "electrician",
        "location": 12345,
        "urgency": null,
        "problem": null,
        "budget": null,
        "customer_intent": "service request",
        "lead_priority": "medium"
    }
    """

    with patch(
        "app.llm.ollama_llm.chat",
        return_value=fake_response,
    ):

        with pytest.raises(ValidationError):
            extract_lead(
                "I need an electrician."
            )




def test_save_lead():
    lead = LeadInformation(
        service="electrician",
        location="Kozhikode",
        urgency="tomorrow",
        problem="wiring problem",
        budget=None,
        customer_intent="service_request",
        lead_priority="high",
    )

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

    with patch(
        "app.services.lead_service.create_lead",
        return_value=fake_saved_lead,
    ) as mock_repository:
        result = save_lead(lead)

    assert result == fake_saved_lead

    mock_repository.assert_called_once_with(
        service="electrician",
        location="Kozhikode",
        urgency="tomorrow",
        problem="wiring problem",
        budget=None,
        customer_intent="service_request",
        lead_priority="high",
    )


def test_save_lead_requires_service_or_location():
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
        "app.services.lead_service.create_lead"
    ) as mock_repository:
        try:
            save_lead(lead)
            assert False
        except ValueError as exc:
            assert str(exc) == (
                "Cannot save lead without service or location"
            )

        mock_repository.assert_not_called()


def test_save_lead_allows_missing_location():
    lead = LeadInformation(
        service="electrician",
        location=None,
        urgency="tomorrow",
        problem="wiring problem",
        budget=None,
        customer_intent="service_request",
        lead_priority="high",
    )

    fake_saved_lead = (
        1,
        "electrician",
        None,
        "tomorrow",
        "wiring problem",
        None,
        "service_request",
        "high",
        "NEW",
        None,
    )

    with patch(
        "app.services.lead_service.create_lead",
        return_value=fake_saved_lead,
    ) as mock_repository:
        result = save_lead(lead)

    assert result == fake_saved_lead

    mock_repository.assert_called_once_with(
        service="electrician",
        location=None,
        urgency="tomorrow",
        problem="wiring problem",
        budget=None,
        customer_intent="service_request",
        lead_priority="high",
    )