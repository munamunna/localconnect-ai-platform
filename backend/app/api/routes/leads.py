from fastapi import APIRouter, HTTPException

from app.schemas.lead import (
    ChatRequest,
    LeadMatchResponse,
)

from app.schemas.freelancer import (
    FreelancerResponse,
)

from app.services.lead_service import (
    extract_lead,
    save_lead,
)

from app.services.lead_matching_service import (
    match_lead_to_freelancers,
)


router = APIRouter(
    tags=["Leads"],
)


@router.post("/extract")
def extract_customer_lead(
    request: ChatRequest,
):
    try:
        lead = extract_lead(
            request.message
        )

        saved_lead = save_lead(
            lead
        )

        return {
            "message": request.message,
            "lead": lead.model_dump(
                mode="json"
            ),
            "lead_id": saved_lead[0],
            "status": saved_lead[8],
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Lead extraction failed: {str(exc)}",
        )


@router.post(
    "/match",
    response_model=LeadMatchResponse,
)
def match_customer_lead(
    request: ChatRequest,
):
    try:
        lead = extract_lead(
            request.message
        )

        freelancers = match_lead_to_freelancers(
            lead
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

        return LeadMatchResponse(
            message=request.message,
            lead=lead,
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
            detail=f"Lead matching failed: {str(exc)}",
        )