from app.services.rag_service import retrieve_knowledge


def build_rag_context(
    query: str,
    limit: int = 5,
) -> str:
    """
    Retrieve relevant knowledge and build a text context
    that can later be provided to an LLM.
    """

    if not query or not query.strip():
        raise ValueError("Query is required")

    documents = retrieve_knowledge(
        query=query,
        limit=limit,
    )

    if not documents:
        return ""

    context_parts = []

    for document in documents:
        content = document[1]

        if content:
            context_parts.append(content.strip())

    return "\n\n".join(context_parts)