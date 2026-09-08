from pydantic import BaseModel


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