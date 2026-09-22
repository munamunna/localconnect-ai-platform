from app.schemas.agent import AgentCapability


def detect_capability(query: str) -> AgentCapability:
    if not query or not query.strip():
        raise ValueError("Query is required")

    normalized_query = query.strip().lower()

    freelancer_search_phrases = (
        "find a freelancer",
        "find an freelancer",
        "find me a freelancer",
        "find someone",
        "find me someone",
        "looking for a freelancer",
        "looking for someone",
        "need a freelancer",
        "need someone",
    )

    freelancer_search_patterns = (
        "find a ",
        "find an ",
        "find me a ",
        "find me an ",
        "looking for a ",
        "looking for an ",
        "need a ",
        "need an ",
    )

    lead_management_keywords = (
        "create lead",
        "create a lead",
        "new lead",
        "add lead",
        "manage lead",
    )

    if any(
        phrase in normalized_query
        for phrase in freelancer_search_phrases
    ):
        return AgentCapability.FREELANCER_SEARCH

    if any(
        normalized_query.startswith(pattern)
        for pattern in freelancer_search_patterns
    ):
        return AgentCapability.FREELANCER_SEARCH

    if any(
        keyword in normalized_query
        for keyword in lead_management_keywords
    ):
        return AgentCapability.LEAD_MANAGEMENT

    return AgentCapability.RAG