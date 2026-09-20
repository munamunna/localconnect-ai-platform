from typing import Any

from app.database.knowledge_repository import create_knowledge_document
from app.services.embedding_service import generate_embedding


def create_knowledge(
    content: str,
    source: str | None = None,
    metadata: dict[str, Any] | None = None,
):
    if not content or not content.strip():
        raise ValueError("Content is required")

    embedding = generate_embedding(content)

    return create_knowledge_document(
        content=content,
        embedding=embedding,
        source=source,
        metadata=metadata,
    )