from unittest.mock import patch

import pytest

from app.services.rag_context_service import build_rag_context


def test_build_rag_context_success():
    documents = [
        (
            1,
            "Plumbing services include pipe repair.",
            "service_catalog",
            {"service": "plumbing"},
            0.91,
        ),
        (
            2,
            "Bathroom plumbing includes leakage fixing.",
            "service_catalog",
            {"service": "plumbing"},
            0.87,
        ),
    ]

    with patch(
        "app.services.rag_context_service.retrieve_knowledge",
        return_value=documents,
    ) as mock_retrieve:

        result = build_rag_context(
            query="My bathroom pipe is leaking",
            limit=5,
        )

    assert result == (
        "Plumbing services include pipe repair.\n\n"
        "Bathroom plumbing includes leakage fixing."
    )

    mock_retrieve.assert_called_once_with(
        query="My bathroom pipe is leaking",
        limit=5,
    )


def test_build_rag_context_returns_empty_string_when_no_documents():
    with patch(
        "app.services.rag_context_service.retrieve_knowledge",
        return_value=[],
    ):

        result = build_rag_context(
            query="Something unrelated",
        )

    assert result == ""


def test_build_rag_context_requires_query():
    with pytest.raises(
        ValueError,
        match="Query is required",
    ):
        build_rag_context("")


def test_build_rag_context_requires_non_whitespace_query():
    with pytest.raises(
        ValueError,
        match="Query is required",
    ):
        build_rag_context("   ")