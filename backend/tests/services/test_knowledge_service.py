from unittest.mock import patch

import pytest

from app.services.knowledge_service import create_knowledge


def test_create_knowledge_success():
    embedding = [0.1] * 768

    expected = (
        1,
        "Plumbing services include pipe repair.",
        "service_catalog",
        {"service": "plumbing"},
        embedding,
        None,
    )

    with patch(
        "app.services.knowledge_service.generate_embedding",
        return_value=embedding,
    ) as mock_embedding, patch(
        "app.services.knowledge_service.create_knowledge_document",
        return_value=expected,
    ) as mock_repository:

        result = create_knowledge(
            content="Plumbing services include pipe repair.",
            source="service_catalog",
            metadata={"service": "plumbing"},
        )

    assert result == expected

    mock_embedding.assert_called_once_with(
        "Plumbing services include pipe repair."
    )

    mock_repository.assert_called_once_with(
        content="Plumbing services include pipe repair.",
        embedding=embedding,
        source="service_catalog",
        metadata={"service": "plumbing"},
    )


def test_create_knowledge_requires_content():
    with pytest.raises(
        ValueError,
        match="Content is required",
    ):
        create_knowledge(
            content="",
        )