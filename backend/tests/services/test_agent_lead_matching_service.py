from unittest.mock import patch

from app.schemas.lead import LeadInformation
from app.services.agent_lead_matching_service import (
    create_lead_and_find_freelancers,
)


def test_create_lead_and_find_freelancers_success():
    lead = LeadInformation(
        service="electrician",
        location="Kozhikode",
        urgency="tomorrow",
        problem="wiring problem",
        customer_intent="service_request",
        lead_priority="high",
    )

    matches = [
        (
            1,
            "Ahmed",
            "electrical",
            "Kozhikode",
            "9876543210",
            True,
            True,
            None,
        )
    ]

    with patch(
        "app.services.agent_lead_matching_service.create_lead_from_message",
        return_value=lead,
    ) as mock_create_lead, patch(
        "app.services.agent_lead_matching_service.search_freelancers",
        return_value=matches,
    ) as mock_search:

        result_lead, result_matches = (
            create_lead_and_find_freelancers(
                "I need an electrician in Kozhikode tomorrow."
            )
        )

    assert result_lead == lead
    assert result_matches == matches

    mock_create_lead.assert_called_once_with(
        "I need an electrician in Kozhikode tomorrow."
    )

    mock_search.assert_called_once_with(
        service="electrician",
        location="Kozhikode",
    )


def test_create_lead_and_find_freelancers_without_service():
    lead = LeadInformation(
        location="Kozhikode",
    )

    with patch(
        "app.services.agent_lead_matching_service.create_lead_from_message",
        return_value=lead,
    ) as mock_create_lead, patch(
        "app.services.agent_lead_matching_service.search_freelancers",
    ) as mock_search:

        result_lead, result_matches = (
            create_lead_and_find_freelancers(
                "I need someone in Kozhikode."
            )
        )

    assert result_lead == lead
    assert result_matches == []

    mock_create_lead.assert_called_once()
    mock_search.assert_not_called()


def test_create_lead_and_find_freelancers_without_location():
    lead = LeadInformation(
        service="electrician",
    )

    with patch(
        "app.services.agent_lead_matching_service.create_lead_from_message",
        return_value=lead,
    ) as mock_create_lead, patch(
        "app.services.agent_lead_matching_service.search_freelancers",
    ) as mock_search:

        result_lead, result_matches = (
            create_lead_and_find_freelancers(
                "I need an electrician."
            )
        )

    assert result_lead == lead
    assert result_matches == []

    mock_create_lead.assert_called_once()
    mock_search.assert_not_called()


def test_create_lead_and_find_freelancers_rejects_empty_message():
    import pytest

    with pytest.raises(ValueError, match="Message is required"):
        create_lead_and_find_freelancers("")


def test_create_lead_and_find_freelancers_rejects_whitespace_message():
    import pytest

    with pytest.raises(ValueError, match="Message is required"):
        create_lead_and_find_freelancers("   ")