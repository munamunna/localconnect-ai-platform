from app.services.agent_freelancer_service import search_freelancers


def check_freelancer_availability(
    service: str,
    location: str,
):
    if not service or not service.strip():
        raise ValueError("Service is required")

    if not location or not location.strip():
        raise ValueError("Location is required")

    return search_freelancers(
        service=service.strip(),
        location=location.strip(),
    )