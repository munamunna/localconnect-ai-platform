from app.schemas.agent import FreelancerSearchRequest
from app.services.freelancer_service import match_freelancers
from app.schemas.agent import FreelancerSearchRequest


def search_freelancers(
    service: str,
    location: str,
):
    if not service or not service.strip():
        raise ValueError("Service is required")

    if not location or not location.strip():
        raise ValueError("Location is required")

    return match_freelancers(
        service=service.strip(),
        location=location.strip(),
    )


def search_freelancers_from_request(
    request: FreelancerSearchRequest,
):
    return search_freelancers(
        service=request.service,
        location=request.location,
    )

def test_search_freelancers_from_request():
    request = FreelancerSearchRequest(
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
        "app.services.agent_freelancer_service.search_freelancers",
        return_value=expected,
    ) as mock_search:

        result = search_freelancers_from_request(request)

    assert result == expected

    mock_search.assert_called_once_with(
        service="Plumbing",
        location="Kozhikode",
    )