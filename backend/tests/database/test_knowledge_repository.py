from unittest.mock import MagicMock, patch

import pytest

from app.database.knowledge_repository import (
    create_knowledge_document,
)


def test_create_knowledge_document_success():
    expected = (
        1,
        "Plumbing services include pipe repair.",
        "service_catalog",
        {"service": "plumbing"},
        [0.1] * 768,
        None,
    )

    mock_connection = MagicMock()
    mock_cursor = mock_connection.cursor.return_value.__enter__.return_value

    mock_cursor.fetchone.return_value = expected

    with patch(
        "app.database.knowledge_repository.get_connection",
        return_value=mock_connection,
    ), patch(
        "app.database.knowledge_repository.register_vector"
    ) as mock_register_vector:

        result = create_knowledge_document(
            content="Plumbing services include pipe repair.",
            embedding=[0.1] * 768,
            source="service_catalog",
            metadata={"service": "plumbing"},
        )

    assert result == expected

    mock_register_vector.assert_called_once_with(
        mock_connection
    )

    mock_cursor.execute.assert_called_once()

    mock_connection.commit.assert_called_once()

    mock_connection.close.assert_called_once()


def test_create_knowledge_document_requires_content():
    with pytest.raises(
        ValueError,
        match="Content is required",
    ):
        create_knowledge_document(
            content="",
            embedding=[0.1] * 768,
        )


def test_create_knowledge_document_requires_768_dimensions():
    with pytest.raises(
        ValueError,
        match="Embedding must contain 768 dimensions",
    ):
        create_knowledge_document(
            content="Plumbing services",
            embedding=[0.1] * 767,
        )