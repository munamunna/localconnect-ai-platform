from unittest.mock import patch

import pytest

from app.services.rag_response_service import generate_rag_response


def test_generate_rag_response_success():
    context = (
        "Plumbing services include pipe repair, "
        "leakage fixing and bathroom plumbing."
    )

    with patch(
        "app.services.rag_response_service.build_rag_context",
        return_value=context,
    ) as mock_context, patch(
        "app.services.rag_response_service.generate_text_response",
        return_value="We can help with your bathroom plumbing issue.",
    ) as mock_llm:

        result = generate_rag_response(
            query="My bathroom pipe is leaking",
            limit=5,
        )

    assert result == (
        "We can help with your bathroom plumbing issue."
    )

    mock_context.assert_called_once_with(
        query="My bathroom pipe is leaking",
        limit=5,
    )

    mock_llm.assert_called_once()

    call_arguments = mock_llm.call_args.kwargs

    assert "My bathroom pipe is leaking" in call_arguments["user_message"]
    assert "Plumbing services include pipe repair" in (
        call_arguments["user_message"]
    )


def test_generate_rag_response_returns_fallback_without_context():
    with patch(
        "app.services.rag_response_service.build_rag_context",
        return_value="",
    ) as mock_context, patch(
        "app.services.rag_response_service.generate_text_response",
    ) as mock_llm:

        result = generate_rag_response(
            query="Something unrelated",
        )

    assert result == "I don't have enough information to answer that."

    mock_context.assert_called_once_with(
        query="Something unrelated",
        limit=5,
    )

    mock_llm.assert_not_called()


def test_generate_rag_response_requires_query():
    with pytest.raises(
        ValueError,
        match="Query is required",
    ):
        generate_rag_response("")


def test_generate_rag_response_requires_non_whitespace_query():
    with pytest.raises(
        ValueError,
        match="Query is required",
    ):
        generate_rag_response("   ")