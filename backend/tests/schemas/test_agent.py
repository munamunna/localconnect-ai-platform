import pytest
from pydantic import ValidationError

from app.schemas.agent import FreelancerSearchRequest


def test_freelancer_search_request():
    request = FreelancerSearchRequest(
        service="Plumbing",
        location="Kozhikode",
    )

    assert request.service == "Plumbing"
    assert request.location == "Kozhikode"


def test_freelancer_search_request_requires_service():
    with pytest.raises(ValidationError):
        FreelancerSearchRequest(
            location="Kozhikode",
        )


def test_freelancer_search_request_requires_location():
    with pytest.raises(ValidationError):
        FreelancerSearchRequest(
            service="Plumbing",
        )