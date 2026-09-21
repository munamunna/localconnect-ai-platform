from enum import Enum


class AgentCapability(str, Enum):
    RAG = "rag"
    FREELANCER_SEARCH = "freelancer_search"
    LEAD_MANAGEMENT = "lead_management"