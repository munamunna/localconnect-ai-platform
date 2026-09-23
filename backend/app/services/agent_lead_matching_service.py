from app.services.agent_availability_service import (
    check_freelancer_availability,
)
from app.services.agent_lead_service import create_lead_from_message


def create_lead_and_find_freelancers(message: str):
    if not message or not message.strip():
        raise ValueError("Message is required")

    lead = create_lead_from_message(message.strip())

    if not lead.service or not lead.location:
        return lead, []

    matches = check_freelancer_availability(
        service=lead.service,
        location=lead.location,
    )

    return lead, matches