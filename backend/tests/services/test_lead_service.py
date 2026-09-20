from unittest.mock import patch

from app.schemas.lead import LeadInformation
from app.services.lead_service import extract_lead, save_lead


def test_extract_lead_success():
    mock_response = """
    {
        "service": "electrician",
        "location": "Kozhikode",
        "urgency": "tomorrow",
        "problem": "wiring problem",
        "budget": null,
        "customer_intent": "service_request",
        "lead_priority": "high"
    }
    """

    with patch(
        "app.services.lead_service.generate_structured_response",
        return_value=mock_response,
    ) as mock_llm:

        result = extract_lead(
            "I need an electrician in Kozhikode tomorrow"
        )

    assert isinstance(result, LeadInformation)

    assert result.service == "electrician"
    assert result.location == "Kozhikode"
    assert result.urgency == "tomorrow"
    assert result.problem == "wiring problem"
    assert result.budget is None
    assert result.customer_intent == "service_request"
    assert result.lead_priority == "high"

    mock_llm.assert_called_once()


def test_extract_lead_missing_fields():
    mock_response = """
    {
        "service": "plumber",
        "location": null,
        "urgency": null,
        "problem": null,
        "budget": null,
        "customer_intent": "service_request",
        "lead_priority": "low"
    }
    """

    with patch(
        "app.services.lead_service.generate_structured_response",
        return_value=mock_response,
    ):

        result = extract_lead(
            "I need a plumber"
        )

    assert result.service == "plumber"
    assert result.location is None
    assert result.urgency is None
    assert result.problem is None
    assert result.budget is None
    assert result.customer_intent == "service_request"
    assert result.lead_priority == "low"


def test_extract_lead_invalid_llm_response():
    mock_response = """
    {
        "service": "electrician",
        "location": "Kozhikode",
    """

    with patch(
        "app.services.lead_service.generate_structured_response",
        return_value=mock_response,
    ):

        try:
            extract_lead(
                "I need an electrician"
            )
            assert False, "Expected validation/parsing error"
        except Exception:
            assert True


def test_save_lead_success():
    lead = LeadInformation(
        service="electrician",
        location="Kozhikode",
        urgency="tomorrow",
        problem="wiring problem",
        budget=None,
        customer_intent="service_request",
        lead_priority="high",
    )

    mock_saved_lead = (
        1,
        "electrician",
        "Kozhikode",
        "tomorrow",
        "wiring problem",
        None,
        "service_request",
        "high",
        "new",
    )

    with patch(
        "app.services.lead_service.create_lead",
        return_value=mock_saved_lead,
    ) as mock_repository:

        result = save_lead(lead)

    assert result == mock_saved_lead

    mock_repository.assert_called_once_with(
        service="electrician",
        location="Kozhikode",
        urgency="tomorrow",
        problem="wiring problem",
        budget=None,
        customer_intent="service_request",
        lead_priority="high",
    )


def test_save_lead_without_service_and_location():
    lead = LeadInformation(
        service=None,
        location=None,
    )

    try:
        save_lead(lead)
        assert False, "Expected ValueError"
    except ValueError as exc:
        assert str(exc) == (
            "Cannot save lead without service or location"
        )


def test_save_lead_with_service_only():
    lead = LeadInformation(
        service="electrician",
        location=None,
    )

    mock_saved_lead = (
        1,
        "electrician",
        None,
        None,
        None,
        None,
        None,
        None,
        "new",
    )

    with patch(
        "app.services.lead_service.create_lead",
        return_value=mock_saved_lead,
    ) as mock_repository:

        result = save_lead(lead)

    assert result == mock_saved_lead

    mock_repository.assert_called_once_with(
        service="electrician",
        location=None,
        urgency=None,
        problem=None,
        budget=None,
        customer_intent=None,
        lead_priority=None,
    )


def test_save_lead_with_location_only():
    lead = LeadInformation(
        service=None,
        location="Kozhikode",
    )

    mock_saved_lead = (
        1,
        None,
        "Kozhikode",
        None,
        None,
        None,
        None,
        None,
        "new",
    )

    with patch(
        "app.services.lead_service.create_lead",
        return_value=mock_saved_lead,
    ) as mock_repository:

        result = save_lead(lead)

    assert result == mock_saved_lead

    mock_repository.assert_called_once_with(
        service=None,
        location="Kozhikode",
        urgency=None,
        problem=None,
        budget=None,
        customer_intent=None,
        lead_priority=None,
    )