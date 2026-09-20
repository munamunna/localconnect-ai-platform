from __future__ import annotations


SERVICE_ALIASES: dict[str, str] = {
    # Web / App Development
    "web and app": "web and app",
    "web and app development": "web and app",
    "web app development": "web and app",
    "website and app development": "web and app",
    "website and mobile app development": "web and app",
    "web development": "web and app",
    "website development": "web and app",
    "app development": "web and app",
    "application development": "web and app",

    # Plumbing
    "plumber": "plumbing",
    "plumbing": "plumbing",
    "pipe repair": "plumbing",
    "pipe leakage": "plumbing",
    "water pipe repair": "plumbing",

    # Electrical
    "electrician": "electrical",
    "electrical": "electrical",
    "electrical work": "electrical",
    "wiring": "electrical",
    "house wiring": "electrical",

    # Painting
    "painter": "painting",
    "painting": "painting",
    "house painting": "painting",
    "wall painting": "painting",

    # Carpentry
    "carpenter": "carpentry",
    "carpentry": "carpentry",
    "wood work": "carpentry",
    "woodworking": "carpentry",

    # AC
    "ac technician": "ac service",
    "air conditioner service": "ac service",
    "air conditioning service": "ac service",
    "ac repair": "ac service",
    "ac service": "ac service",
}


def normalize_service(service: str) -> str:
    """
    Convert a user/freelancer-provided service name
    into a canonical LocalConnect service name.
    """

    if not service or not service.strip():
        raise ValueError("Service is required")

    normalized = " ".join(service.strip().lower().split())

    return SERVICE_ALIASES.get(normalized, normalized)