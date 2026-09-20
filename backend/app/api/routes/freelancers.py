from fastapi import APIRouter, HTTPException

from app.schemas.freelancer import (
    FreelancerAvailabilityUpdate,
    FreelancerCreate,
    FreelancerMatchRequest,
    FreelancerMatchResponse,
    FreelancerResponse,
)

from app.services.freelancer_service import (
    match_freelancers,
    register_freelancer,
    verify_freelancer_profile,
    update_freelancer_availability_status,
)


router = APIRouter(
    tags=["Freelancers"],
)


@router.post(
    "/match",
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


@router.post(
    "",
    response_model=FreelancerResponse,
    status_code=201,
)
def create_freelancer_profile(
    request: FreelancerCreate,
):
    try:
        freelancer = register_freelancer(
            name=request.name,
            service=request.service,
            location=request.location,
            phone=request.phone,
        )

        return {
            "id": freelancer[0],
            "name": freelancer[1],
            "service": freelancer[2],
            "location": freelancer[3],
            "phone": freelancer[4],
            "verified": freelancer[5],
            "available": freelancer[6],
            "created_at": freelancer[7],
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )


@router.post(
    "/{freelancer_id}/verify",
    response_model=FreelancerResponse,
)
def verify_freelancer_endpoint(
    freelancer_id: int,
):
    try:
        freelancer = verify_freelancer_profile(
            freelancer_id
        )

        return {
            "id": freelancer[0],
            "name": freelancer[1],
            "service": freelancer[2],
            "location": freelancer[3],
            "phone": freelancer[4],
            "verified": freelancer[5],
            "available": freelancer[6],
            "created_at": freelancer[7],
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )


@router.patch(
    "/{freelancer_id}/availability",
    response_model=FreelancerResponse,
)
def update_freelancer_availability_endpoint(
    freelancer_id: int,
    request: FreelancerAvailabilityUpdate,
):
    try:
        freelancer = update_freelancer_availability_status(
            freelancer_id=freelancer_id,
            available=request.available,
        )

        return {
            "id": freelancer[0],
            "name": freelancer[1],
            "service": freelancer[2],
            "location": freelancer[3],
            "phone": freelancer[4],
            "verified": freelancer[5],
            "available": freelancer[6],
            "created_at": freelancer[7],
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )