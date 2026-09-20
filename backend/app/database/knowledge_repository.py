from typing import Any

from pgvector.psycopg import register_vector
from psycopg.types.json import Jsonb

from app.database.connection import get_connection


def create_knowledge_document(
    content: str,
    embedding: list[float],
    source: str | None = None,
    metadata: dict[str, Any] | None = None,
):
    if not content or not content.strip():
        raise ValueError("Content is required")

    if len(embedding) != 768:
        raise ValueError("Embedding must contain 768 dimensions")

    connection = get_connection()

    try:
        register_vector(connection)

        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO knowledge_documents
                    (content, source, metadata, embedding)
                VALUES
                    (%s, %s, %s, %s)
                RETURNING
                    id,
                    content,
                    source,
                    metadata,
                    embedding,
                    created_at;
                """,
                (
                    content.strip(),
                    source,
                    Jsonb(metadata) if metadata is not None else None,
                    embedding,
                ),
            )

            document = cursor.fetchone()

        connection.commit()

        return document

    finally:
        connection.close()