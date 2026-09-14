from app.schemas.lead import LeadInformation
from app.services.freelancer_service import match_freelancers


def match_lead_to_freelancers(
    lead: LeadInformation,
):
    if not lead.service:
        raise ValueError(
            "Cannot match freelancers without a service"
        )

    if not lead.location:
        raise ValueError(
            "Cannot match freelancers without a location"
        )

    return match_freelancers(
        service=lead.service,
        location=lead.location,
    )