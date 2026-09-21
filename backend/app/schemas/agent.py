from enum import Enum

from pydantic import BaseModel


class AgentCapability(str, Enum):
    RAG = "rag"
    FREELANCER_SEARCH = "freelancer_search"
    LEAD_MANAGEMENT = "lead_management"


class FreelancerSearchRequest(BaseModel):
    service: str
    location: str