from app.schemas.agent_lead_response import AgentLeadResponse
from app.schemas.lead import LeadInformation
from app.services.agent_lead_response_service import (
    format_agent_lead_response,
)


def test_format_agent_lead_response():
    lead = LeadInformation(
        service="electrician",
        location="Kozhikode",
        urgency="tomorrow",
        problem="wiring problem",
        budget=None,
        customer_intent="service_request",
        lead_priority="high",
    )

    result = format_agent_lead_response(lead)

    assert isinstance(result, AgentLeadResponse)
    assert result.message == "Lead created successfully."
    assert result.lead == lead


def test_format_agent_lead_response_preserves_lead_data():
    lead = LeadInformation(
        service="plumber",
        location="Kochi",
        urgency="today",
        problem="water leakage",
        budget="AED 500",
        customer_intent="service_request",
        lead_priority="medium",
    )

    result = format_agent_lead_response(lead)

    assert result.lead.service == "plumber"
    assert result.lead.location == "Kochi"
    assert result.lead.urgency == "today"
    assert result.lead.problem == "water leakage"
    assert result.lead.budget == "AED 500"
    assert result.lead.customer_intent == "service_request"
    assert result.lead.lead_priority == "medium"