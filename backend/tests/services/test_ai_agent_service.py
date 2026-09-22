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


def test_run_agent_uses_freelancer_search_and_formats_response():
    search_response = FreelancerSearchResponse(
        message="I found 1 freelancer matching your request.",
        freelancers=[
            FreelancerResult(
                id=110,
                name="muna",
                service="web and app",
                location="payyoli",
                phone="string",
                verified=True,
                available=True,
            )
        ],
    )

    with patch(
        "app.services.ai_agent_service.detect_capability",
        return_value=AgentCapability.FREELANCER_SEARCH,
    ) as mock_detect, patch(
        "app.services.ai_agent_service.extract_freelancer_search_parameters",
    ) as mock_extract, patch(
        "app.services.ai_agent_service.search_freelancers_from_request",
        return_value=[
            (
                110,
                "muna",
                "web and app",
                "payyoli",
                "string",
                True,
                True,
                None,
            )
        ],
    ) as mock_search, patch(
        "app.services.ai_agent_service.format_freelancer_search_response",
        return_value=search_response,
    ) as mock_format:

        from app.schemas.agent import FreelancerSearchRequest

        search_request = FreelancerSearchRequest(
            service="web and app",
            location="payyoli",
        )

        mock_extract.return_value = search_request

        result = run_agent(
            query="Find me a web and app freelancer in Payyoli",
        )

    assert result == search_response

    mock_detect.assert_called_once_with(
        "Find me a web and app freelancer in Payyoli",
    )

    mock_extract.assert_called_once_with(
        "Find me a web and app freelancer in Payyoli",
    )

    mock_search.assert_called_once_with(
        search_request,
    )

    mock_format.assert_called_once_with(
        mock_search.return_value,
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