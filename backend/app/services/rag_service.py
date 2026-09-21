from app.database.knowledge_repository import (
    search_knowledge_documents,
)
from app.services.embedding_service import generate_embedding


def retrieve_knowledge(
    query: str,
    limit: int = 5,
):
    if not query or not query.strip():
        raise ValueError("Query is required")

    if limit <= 0:
        raise ValueError("Limit must be greater than zero")

    query_embedding = generate_embedding(query)

    return search_knowledge_documents(
        query_embedding=query_embedding,
        limit=limit,
    )