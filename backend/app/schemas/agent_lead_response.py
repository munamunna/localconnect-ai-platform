from pydantic import BaseModel

from app.schemas.agent_response import FreelancerResult
from app.schemas.lead import LeadInformation


class AgentLeadResponse(BaseModel):
    message: str
    lead: LeadInformation
    matches: list[FreelancerResult]