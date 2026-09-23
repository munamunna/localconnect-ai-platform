from app.schemas.agent_lead_response import AgentLeadResponse
from app.schemas.lead import LeadInformation
from app.services.agent_lead_response_service import (
    format_agent_lead_response,
)


def test_format_agent_lead_response_with_matches():
    lead = LeadInformation(
        service="electrician",
        location="Kozhikode",
        urgency="tomorrow",
        problem="wiring problem",
        budget=None,
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
        ),
    ]

    result = format_agent_lead_response(
        lead=lead,
        matches=matches,
    )

    assert isinstance(result, AgentLeadResponse)
    assert result.message == (
        "Lead created successfully. "
        "I found 1 matching freelancer."
    )

    assert result.lead == lead
    assert len(result.matches) == 1

    assert result.matches[0].id == 1
    assert result.matches[0].name == "Ahmed"
    assert result.matches[0].service == "electrical"
    assert result.matches[0].location == "Kozhikode"
    assert result.matches[0].phone == "9876543210"
    assert result.matches[0].verified is True
    assert result.matches[0].available is True


def test_format_agent_lead_response_without_matches():
    lead = LeadInformation(
        service="plumber",
        location="Kochi",
    )

    result = format_agent_lead_response(
        lead=lead,
        matches=[],
    )

    assert result.message == (
        "Lead created successfully, "
        "but no matching freelancers were found."
    )

    assert result.lead == lead
    assert result.matches == []


def test_format_agent_lead_response_with_multiple_matches():
    lead = LeadInformation(
        service="electrician",
        location="Kozhikode",
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
        ),
        (
            2,
            "Rahman",
            "electrical",
            "Kozhikode",
            "9876543211",
            True,
            False,
            None,
        ),
    ]

    result = format_agent_lead_response(
        lead=lead,
        matches=matches,
    )

    assert result.message == (
        "Lead created successfully. "
        "I found 2 matching freelancers."
    )

    assert len(result.matches) == 2
    assert result.matches[0].name == "Ahmed"
    assert result.matches[1].name == "Rahman"