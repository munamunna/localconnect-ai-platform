from unittest.mock import patch

import pytest

from app.schemas.lead import LeadInformation
from app.services.agent_lead_service import create_lead_from_message


def test_create_lead_from_message_success():
    lead = LeadInformation(
        service="electrician",
        location="Kozhikode",
        urgency="tomorrow",
        problem="wiring problem",
        budget=None,
        customer_intent="service_request",
        lead_priority="high",
    )

    with patch(
        "app.services.agent_lead_service.extract_lead",
        return_value=lead,
    ) as mock_extract, patch(
        "app.services.agent_lead_service.save_lead",
    ) as mock_save:

        result = create_lead_from_message(
            "I need an electrician in Kozhikode tomorrow."
        )

        assert result == lead

        mock_extract.assert_called_once_with(
            "I need an electrician in Kozhikode tomorrow."
        )

        mock_save.assert_called_once_with(lead)


def test_create_lead_from_message_strips_message():
    lead = LeadInformation(
        service="plumber",
        location="Kozhikode",
    )

    with patch(
        "app.services.agent_lead_service.extract_lead",
        return_value=lead,
    ) as mock_extract, patch(
        "app.services.agent_lead_service.save_lead",
    ):

        create_lead_from_message(
            "   I need a plumber in Kozhikode   "
        )

        mock_extract.assert_called_once_with(
            "I need a plumber in Kozhikode"
        )


def test_create_lead_from_message_rejects_empty_message():
    with pytest.raises(ValueError, match="Message is required"):
        create_lead_from_message("")


def test_create_lead_from_message_rejects_whitespace_message():
    with pytest.raises(ValueError, match="Message is required"):
        create_lead_from_message("   ")