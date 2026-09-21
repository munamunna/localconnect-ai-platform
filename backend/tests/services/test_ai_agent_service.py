from unittest.mock import patch

import pytest

from app.schemas.agent import (
    AgentCapability,
    FreelancerSearchRequest,
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


def test_run_agent_uses_freelancer_search():
    search_request = FreelancerSearchRequest(
        service="Plumbing",
        location="Kozhikode",
    )

    expected = [
        (
            1,
            "Ahmed",
            "Plumbing",
            "Kozhikode",
            "9876543210",
            True,
            True,
            None,
        )
    ]

    with patch(
        "app.services.ai_agent_service.detect_capability",
        return_value=AgentCapability.FREELANCER_SEARCH,
    ) as mock_detect, patch(
        "app.services.ai_agent_service.search_freelancers_from_request",
        return_value=expected,
    ) as mock_search:

        result = run_agent(
            query="Find a plumber in Kozhikode",
            freelancer_search=search_request,
        )

    assert result == expected

    mock_detect.assert_called_once_with(
        "Find a plumber in Kozhikode",
    )

    mock_search.assert_called_once_with(
        search_request,
    )


def test_run_agent_requires_freelancer_search_parameters():
    with patch(
        "app.services.ai_agent_service.detect_capability",
        return_value=AgentCapability.FREELANCER_SEARCH,
    ):

        with pytest.raises(
            ValueError,
            match="Freelancer search parameters are required",
        ):
            run_agent(
                query="Find a plumber in Kozhikode",
            )


def test_run_agent_identifies_lead_management():
    with patch(
        "app.services.ai_agent_service.detect_capability",
        return_value=AgentCapability.LEAD_MANAGEMENT,
    ):

        result = run_agent(
            query="Create a lead for this customer",
        )

    assert result == (
        "Lead management capability is not implemented yet."
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