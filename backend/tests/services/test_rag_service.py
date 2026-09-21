from unittest.mock import patch

import pytest

from app.services.rag_service import retrieve_knowledge


def test_retrieve_knowledge_success():
    embedding = [0.1] * 768

    expected = [
        (
            1,
            "Plumbing services include pipe repair.",
            "service_catalog",
            {"service": "plumbing"},
            0.91,
        )
    ]

    with patch(
        "app.services.rag_service.generate_embedding",
        return_value=embedding,
    ) as mock_embedding, patch(
        "app.services.rag_service.search_knowledge_documents",
        return_value=expected,
    ) as mock_repository:

        result = retrieve_knowledge(
            query="My bathroom pipe is leaking",
            limit=5,
        )

    assert result == expected

    mock_embedding.assert_called_once_with(
        "My bathroom pipe is leaking"
    )

    mock_repository.assert_called_once_with(
        query_embedding=embedding,
        limit=5,
    )


def test_retrieve_knowledge_requires_query():
    with pytest.raises(
        ValueError,
        match="Query is required",
    ):
        retrieve_knowledge("")


def test_retrieve_knowledge_requires_positive_limit():
    with pytest.raises(
        ValueError,
        match="Limit must be greater than zero",
    ):
        retrieve_knowledge(
            query="My bathroom pipe is leaking",
            limit=0,
        )