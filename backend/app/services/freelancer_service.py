from app.database.freelancer_repository import (
    find_matching_freelancers,
)


def match_freelancers(
    service: str,
    location: str,
):
    if not service or not service.strip():
        raise ValueError("Service is required")

    if not location or not location.strip():
        raise ValueError("Location is required")

    return find_matching_freelancers(
        service=service.strip(),
        location=location.strip(),
    )