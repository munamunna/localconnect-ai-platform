from app.database.freelancer_repository import (
    create_freelancer,
    find_matching_freelancers,
    verify_freelancer,
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

def register_freelancer(
    name: str,
    service: str,
    location: str,
    phone: str | None = None,
):
    if not name or not name.strip():
        raise ValueError("Name is required")

    if not service or not service.strip():
        raise ValueError("Service is required")

    if not location or not location.strip():
        raise ValueError("Location is required")

    return create_freelancer(
        name=name.strip(),
        service=service.strip(),
        location=location.strip(),
        phone=phone.strip() if phone else None,
        verified=False,
        available=True,
    )
def verify_freelancer_profile(freelancer_id: int):
    if freelancer_id <= 0:
        raise ValueError("Invalid freelancer ID")

    freelancer = verify_freelancer(freelancer_id)

    if freelancer is None:
        raise ValueError("Freelancer not found")

    return freelancer