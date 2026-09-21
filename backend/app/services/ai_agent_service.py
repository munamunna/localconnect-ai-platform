from app.schemas.agent import (
    AgentCapability,
    FreelancerSearchRequest,
)
from app.services.agent_freelancer_service import (
    search_freelancers_from_request,
)
from app.services.agent_router_service import detect_capability
from app.services.rag_response_service import generate_rag_response


def run_agent(
    query: str,
    limit: int = 5,
    freelancer_search: FreelancerSearchRequest | None = None,
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
        if freelancer_search is None:
            raise ValueError(
                "Freelancer search parameters are required"
            )

        return search_freelancers_from_request(
            freelancer_search
        )

    if capability == AgentCapability.LEAD_MANAGEMENT:
        return "Lead management capability is not implemented yet."

    raise ValueError("Unsupported agent capability")