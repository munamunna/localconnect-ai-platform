from pydantic import BaseModel
from app.schemas.freelancer import FreelancerResponse


class ChatRequest(BaseModel):
    message: str


class LeadInformation(BaseModel):
    service: str | None = None
    location: str | None = None
    urgency: str | None = None
    problem: str | None = None
    budget: str | None = None
    customer_intent: str | None = None
    lead_priority: str | None = None

class LeadMatchResponse(BaseModel):

    message: str

    lead: LeadInformation

    matches: list[FreelancerResponse]