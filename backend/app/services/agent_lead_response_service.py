from app.schemas.agent_lead_response import AgentLeadResponse
from app.schemas.lead import LeadInformation


def format_agent_lead_response(
    lead: LeadInformation,
) -> AgentLeadResponse:
    return AgentLeadResponse(
        message="Lead created successfully.",
        lead=lead,
    )