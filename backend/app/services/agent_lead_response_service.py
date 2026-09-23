from app.schemas.agent_lead_response import AgentLeadResponse
from app.schemas.agent_response import FreelancerResult
from app.schemas.lead import LeadInformation


def format_agent_lead_response(
    lead: LeadInformation,
    matches: list[tuple],
) -> AgentLeadResponse:
    freelancers = []

    for result in matches:
        freelancer = FreelancerResult(
            id=result[0],
            name=result[1],
            service=result[2],
            location=result[3],
            phone=result[4],
            verified=result[5],
            available=result[6],
        )
        freelancers.append(freelancer)

    if freelancers:
        message = (
            f"Lead created successfully. "
            f"I found {len(freelancers)} matching freelancer"
            f"{'s' if len(freelancers) != 1 else ''}."
        )
    else:
        message = (
            "Lead created successfully, "
            "but no matching freelancers were found."
        )

    return AgentLeadResponse(
        message=message,
        lead=lead,
        matches=freelancers,
    )