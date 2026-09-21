from unittest.mock import patch

import pytest

from app.services.ai_agent_service import run_agent


def test_run_agent_success():
    with patch(
        "app.services.ai_agent_service.generate_rag_response",
        return_value="We can help with your plumbing issue.",
    ) as mock_rag:

        result = run_agent(
            query="My bathroom pipe is leaking",
            limit=5,
        )

    assert result == "We can help with your plumbing issue."

    mock_rag.assert_called_once_with(
        query="My bathroom pipe is leaking",
        limit=5,
    )


def test_run_agent_requires_query():
    with pytest.raises(
        ValueError,
        match="Query is required",
    ):
        run_agent("")


def test_run_agent_requires_non_whitespace_query():
    with pytest.raises(
        ValueError,
        match="Query is required",
    ):
        run_agent("   ")


def test_run_agent_passes_limit_to_rag():
    with patch(
        "app.services.ai_agent_service.generate_rag_response",
        return_value="Response",
    ) as mock_rag:

        result = run_agent(
            query="Find plumbing help",
            limit=3,
        )

    assert result == "Response"

    mock_rag.assert_called_once_with(
        query="Find plumbing help",
        limit=3,
    )