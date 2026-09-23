from unittest.mock import patch

import pytest

from app.schemas.agent import AgentCapability
from app.schemas.agent_response import (
    FreelancerResult,
    FreelancerSearchResponse,
)
from app.services.ai_agent_service import run_agent


def test_run_agent_uses_rag_for_rag_capability():
    with patch(
        "app.services.ai_agent_service.detect_capability",
        return_value=AgentCapability.RAG,
    ) as mock_detect, patch(
        "app.services.ai_agent_service.generate_rag_response",
        return_value="We can help with your plumbing issue.",
    ) as mock_rag:

        result = run_agent(
            query="My bathroom pipe is leaking",
            limit=5,
        )

    assert result == "We can help with your plumbing issue."

    mock_detect.assert_called_once_with(
        "My bathroom pipe is leaking",
    )

    mock_rag.assert_called_once_with(
        query="My bathroom pipe is leaking",
        limit=5,
    )


def test_run_agent_identifies_lead_management():
    with patch(
        "app.services.ai_agent_service.detect_capability",
        return_value=AgentCapability.LEAD_MANAGEMENT,
    ), patch(
        "app.services.ai_agent_service.create_lead_from_message",
        return_value="lead-data",
    ) as mock_create_lead, patch(
        "app.services.ai_agent_service.format_agent_lead_response",
        return_value="formatted-response",
    ) as mock_format:

        result = run_agent(
            query="Create a lead for this customer",
        )

        assert result == "formatted-response"

        mock_create_lead.assert_called_once_with(
            "Create a lead for this customer"
        )

        mock_format.assert_called_once_with(
            "lead-data"
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