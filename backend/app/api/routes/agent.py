from fastapi import APIRouter, HTTPException

from app.schemas.agent_chat import (
    AgentChatRequest,
    AgentChatResponse,
)
from app.services.ai_agent_service import run_agent


router = APIRouter(
    tags=["Agent"],
)


@router.post(
    "/chat",
    response_model=AgentChatResponse,
)
def agent_chat(
    request: AgentChatRequest,
):
    try:
        response = run_agent(
            query=request.message,
        )

        return AgentChatResponse(
            response=response,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Agent request failed: {str(exc)}",
        )