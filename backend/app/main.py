
from fastapi import FastAPI, HTTPException

from app.schemas.lead import ChatRequest
from app.services.lead_service import extract_lead


app = FastAPI(
    title="LocalConnect AI Platform",
    version="0.1.0",
)


@app.get("/")
def root():
    return {
        "message": "LocalConnect AI Platform API is running"
    }


@app.post("/api/leads/extract")
def extract_customer_lead(request: ChatRequest):

    try:
        lead = extract_lead(request.message)

        return {
            "message": request.message,
            "lead": lead.model_dump(mode="json"),
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Lead extraction failed: {str(exc)}",
        )