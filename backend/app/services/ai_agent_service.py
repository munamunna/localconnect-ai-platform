from app.services.agent_router_service import detect_capability
from app.services.rag_response_service import generate_rag_response
from app.schemas.agent import AgentCapability


def run_agent(
    query: str,
    limit: int = 5,
) -> str:
    if not query or not query.strip():
        raise ValueError("Query is required")

    capability = detect_capability(query)

    if capability == AgentCapability.RAG:
        return generate_rag_response(
            query=query,
            limit=limit,
        )

    if capability == AgentCapability.FREELANCER_SEARCH:
        return "Freelancer search capability is not implemented yet."

    if capability == AgentCapability.LEAD_MANAGEMENT:
        return "Lead management capability is not implemented yet."

    raise ValueError("Unsupported agent capability")