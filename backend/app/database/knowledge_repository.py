from typing import Any

from pgvector.psycopg import register_vector
from psycopg.types.json import Jsonb

from app.database.connection import get_connection
from pgvector import Vector


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

def search_knowledge_documents(
    query_embedding: list[float],
    limit: int = 5,
):
    if len(query_embedding) != 768:
        raise ValueError(
            "Query embedding must contain 768 dimensions"
        )

    if limit <= 0:
        raise ValueError("Limit must be greater than zero")

    connection = get_connection()

    try:
        register_vector(connection)

        query_vector = Vector(query_embedding)

        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    id,
                    content,
                    source,
                    metadata,
                    1 - (embedding <=> %s) AS similarity
                FROM knowledge_documents
                WHERE embedding IS NOT NULL
                ORDER BY embedding <=> %s
                LIMIT %s;
                """,
                (
                    query_vector,
                    query_vector,
                    limit,
                ),
            )

            documents = cursor.fetchall()

        return documents

    finally:
        connection.close()