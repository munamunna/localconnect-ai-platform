from pydantic import BaseModel

from app.schemas.lead import LeadInformation


class AgentLeadResponse(BaseModel):
    message: str
    lead: LeadInformation