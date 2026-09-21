from app.schemas.agent import AgentCapability


def detect_capability(query: str) -> AgentCapability:
    if not query or not query.strip():
        raise ValueError("Query is required")

    normalized_query = query.strip().lower()

    freelancer_search_keywords = (
        "find freelancer",
        "find a freelancer",
        "find someone",
        "find a plumber",
        "find an electrician",
        "find a painter",
        "find a carpenter",
        "looking for a plumber",
        "looking for an electrician",
        "need a plumber",
        "need an electrician",
        "need a painter",
        "need a carpenter",
    )

    lead_management_keywords = (
        "create lead",
        "create a lead",
        "new lead",
        "add lead",
        "manage lead",
    )

    if any(
        keyword in normalized_query
        for keyword in freelancer_search_keywords
    ):
        return AgentCapability.FREELANCER_SEARCH

    if any(
        keyword in normalized_query
        for keyword in lead_management_keywords
    ):
        return AgentCapability.LEAD_MANAGEMENT

    return AgentCapability.RAG