from unittest.mock import patch

from app.schemas.lead import LeadInformation
from app.services.lead_matching_service import (
    match_lead_to_freelancers,
)


def test_match_lead_to_freelancers():

    lead = LeadInformation(
        service="electrician",
        location="Kozhikode",
        urgency="tomorrow",
        problem="wiring problem",
        budget=None,
        customer_intent="service request",
        lead_priority="high",
    )

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
        "app.services.lead_matching_service.match_freelancers",
        return_value=fake_freelancers,
    ) as mock_match:

        result = match_lead_to_freelancers(lead)

    assert result == fake_freelancers

    mock_match.assert_called_once_with(
        service="electrician",
        location="Kozhikode",
    )

def test_match_lead_requires_service():

    lead = LeadInformation(
        service=None,
        location="Kozhikode",
        urgency=None,
        problem=None,
        budget=None,
        customer_intent=None,
        lead_priority=None,
    )

    with patch(
        "app.services.lead_matching_service.match_freelancers",
    ) as mock_match:

        try:
            match_lead_to_freelancers(lead)
            assert False
        except ValueError as exc:
            assert str(exc) == (
                "Cannot match freelancers without a service"
            )

        mock_match.assert_not_called()


def test_match_lead_requires_location():

    lead = LeadInformation(
        service="electrician",
        location=None,
        urgency=None,
        problem=None,
        budget=None,
        customer_intent=None,
        lead_priority=None,
    )

    with patch(
        "app.services.lead_matching_service.match_freelancers",
    ) as mock_match:

        try:
            match_lead_to_freelancers(lead)
            assert False
        except ValueError as exc:
            assert str(exc) == (
                "Cannot match freelancers without a location"
            )

        mock_match.assert_not_called()