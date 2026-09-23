from app.schemas.agent import AgentCapability
from app.services.agent_freelancer_service import search_freelancers_from_request
from app.services.agent_lead_service import create_lead_from_message
from app.services.agent_parameter_service import extract_freelancer_search_parameters
from app.services.agent_response_service import format_freelancer_search_response
from app.services.agent_router_service import detect_capability
from app.services.rag_response_service import generate_rag_response
from app.services.agent_lead_response_service import (
    format_agent_lead_response,
)


def run_agent(query: str, limit: int = 5):
    if not query or not query.strip():
        raise ValueError("Query is required")

    capability = detect_capability(query)

    if capability == AgentCapability.RAG:
        return generate_rag_response(
            query=query,
            limit=limit,
        )

    if capability == AgentCapability.FREELANCER_SEARCH:
        search_request = extract_freelancer_search_parameters(query)

        results = search_freelancers_from_request(
            search_request
        )

        return format_freelancer_search_response(results)

    if capability == AgentCapability.LEAD_MANAGEMENT:
        lead = create_lead_from_message(query)
        return format_agent_lead_response(lead)

    raise ValueError("Unsupported agent capability")