from unittest.mock import MagicMock, patch

import pytest


from app.database.knowledge_repository import (
    search_knowledge_documents,
)


def test_search_knowledge_documents_success():
    expected = [
        (
            1,
            "Plumbing services include pipe repair.",
            "service_catalog",
            {"service": "plumbing"},
            0.91,
        )
    ]

    mock_connection = MagicMock()
    mock_cursor = (
        mock_connection.cursor.return_value.__enter__.return_value
    )

    mock_cursor.fetchall.return_value = expected

    query_embedding = [0.1] * 768

    with patch(
        "app.database.knowledge_repository.get_connection",
        return_value=mock_connection,
    ), patch(
        "app.database.knowledge_repository.register_vector"
    ) as mock_register_vector:

        result = search_knowledge_documents(
            query_embedding=query_embedding,
            limit=5,
        )

    assert result == expected

    mock_register_vector.assert_called_once_with(
        mock_connection
    )

    mock_cursor.execute.assert_called_once()

    execute_arguments = mock_cursor.execute.call_args.args
    parameters = execute_arguments[1]

    

    assert parameters[0] == parameters[1]
    assert parameters[2] == 5

    mock_connection.close.assert_called_once()


def test_search_knowledge_documents_requires_768_dimensions():
    with pytest.raises(
        ValueError,
        match="Query embedding must contain 768 dimensions",
    ):
        search_knowledge_documents(
            query_embedding=[0.1] * 767,
        )


def test_search_knowledge_documents_requires_positive_limit():
    with pytest.raises(
        ValueError,
        match="Limit must be greater than zero",
    ):
        search_knowledge_documents(
            query_embedding=[0.1] * 768,
            limit=0,
        )