from fastapi import FastAPI, HTTPException

from app.schemas.lead import ChatRequest
from app.schemas.freelancer import (
    FreelancerMatchRequest,
    FreelancerMatchResponse,
    FreelancerResponse,
)
from app.services.lead_service import extract_lead
from app.services.freelancer_service import match_freelancers


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


@app.post(
    "/api/freelancers/match",
    response_model=FreelancerMatchResponse,
)
def match_customer_freelancers(
    request: FreelancerMatchRequest,
):

    try:
        freelancers = match_freelancers(
            service=request.service,
            location=request.location,
        )

        matches = [
            FreelancerResponse(
                id=freelancer[0],
                name=freelancer[1],
                service=freelancer[2],
                location=freelancer[3],
                phone=freelancer[4],
                verified=freelancer[5],
                available=freelancer[6],
                created_at=(
                    freelancer[7].isoformat()
                    if freelancer[7]
                    else None
                ),
            )
            for freelancer in freelancers
        ]

        return FreelancerMatchResponse(
            matches=matches,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Freelancer matching failed: {str(exc)}",
        )