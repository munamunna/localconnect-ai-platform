from app.services.rag_response_service import generate_rag_response


def run_agent(
    query: str,
    limit: int = 5,
) -> str:
    if not query or not query.strip():
        raise ValueError("Query is required")

    return generate_rag_response(
        query=query,
        limit=limit,
    )