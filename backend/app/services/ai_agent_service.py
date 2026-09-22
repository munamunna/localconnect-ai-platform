from app.schemas.agent import AgentCapability
from app.services.agent_freelancer_service import (
    search_freelancers_from_request,
)
from app.services.agent_parameter_service import (
    extract_freelancer_search_parameters,
)
from app.services.agent_response_service import (
    format_freelancer_search_response,
)
from app.services.agent_router_service import detect_capability
from app.services.rag_response_service import generate_rag_response


def run_agent(
    query: str,
    limit: int = 5,
):
    if not query or not query.strip():
        raise ValueError("Query is required")

    capability = detect_capability(query)

    if capability == AgentCapability.RAG:
        return generate_rag_response(
            query=query,
            limit=limit,
        )

    if capability == AgentCapability.FREELANCER_SEARCH:
        search_request = extract_freelancer_search_parameters(
            query
        )

        results = search_freelancers_from_request(
            search_request
        )

        return format_freelancer_search_response(
            results
        )

    if capability == AgentCapability.LEAD_MANAGEMENT:
        return "Lead management capability is not implemented yet."

    raise ValueError("Unsupported agent capability")