from fastapi import APIRouter


router = APIRouter(
    tags=["Health"],
)


@router.get("/")
def root():
    return {
        "message": "LocalConnect AI Platform API is running"
    }