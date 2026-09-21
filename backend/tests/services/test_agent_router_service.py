import pytest

from app.schemas.agent import AgentCapability
from app.services.agent_router_service import detect_capability


def test_detect_rag_capability():
    result = detect_capability(
        "My bathroom pipe is leaking"
    )

    assert result == AgentCapability.RAG


def test_detect_freelancer_search_capability():
    result = detect_capability(
        "Find a plumber for me"
    )

    assert result == AgentCapability.FREELANCER_SEARCH


def test_detect_lead_management_capability():
    result = detect_capability(
        "Create a lead for this customer"
    )

    assert result == AgentCapability.LEAD_MANAGEMENT


def test_detect_capability_requires_query():
    with pytest.raises(
        ValueError,
        match="Query is required",
    ):
        detect_capability("")


def test_detect_capability_requires_non_whitespace_query():
    with pytest.raises(
        ValueError,
        match="Query is required",
    ):
        detect_capability("   ")