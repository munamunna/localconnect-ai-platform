from app.schemas.lead import LeadInformation
from app.services.lead_service import extract_lead, save_lead


def create_lead_from_message(message: str) -> LeadInformation:
    if not message or not message.strip():
        raise ValueError("Message is required")

    lead = extract_lead(message.strip())

    save_lead(lead)

    return lead