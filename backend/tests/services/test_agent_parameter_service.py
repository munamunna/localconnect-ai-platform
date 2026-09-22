from unittest.mock import patch

import pytest

from app.schemas.agent import FreelancerSearchRequest
from app.services.agent_parameter_service import (
    extract_freelancer_search_parameters,
)


def test_extract_freelancer_search_parameters_success():
    llm_response = """
{
    "service": "Plumbing",
    "location": "Kozhikode"
}
"""

    with patch(
        "app.services.agent_parameter_service.generate_structured_response",
        return_value=llm_response,
    ) as mock_llm:

        result = extract_freelancer_search_parameters(
            "Find me a plumber in Kozhikode"
        )

    assert isinstance(result, FreelancerSearchRequest)
    assert result.service == "Plumbing"
    assert result.location == "Kozhikode"

    mock_llm.assert_called_once()


def test_extract_freelancer_search_parameters_strips_query():
    llm_response = """
{
    "service": "Electrical",
    "location": "Kochi"
}
"""

    with patch(
        "app.services.agent_parameter_service.generate_structured_response",
        return_value=llm_response,
    ) as mock_llm:

        result = extract_freelancer_search_parameters(
            "  Find an electrician in Kochi  "
        )

    assert result.service == "Electrical"
    assert result.location == "Kochi"

    call_arguments = mock_llm.call_args.kwargs

    assert call_arguments["user_message"] == (
        "Find an electrician in Kochi"
    )


def test_extract_freelancer_search_parameters_requires_query():
    with pytest.raises(
        ValueError,
        match="Query is required",
    ):
        extract_freelancer_search_parameters("")


def test_extract_freelancer_search_parameters_requires_non_whitespace_query():
    with pytest.raises(
        ValueError,
        match="Query is required",
    ):
        extract_freelancer_search_parameters("   ")


def test_extract_freelancer_search_parameters_validates_llm_output():
    llm_response = """
{
    "service": "Plumbing"
}
"""

    with patch(
        "app.services.agent_parameter_service.generate_structured_response",
        return_value=llm_response,
    ):

        with pytest.raises(ValueError):
            extract_freelancer_search_parameters(
                "Find a plumber in Kozhikode"
            )