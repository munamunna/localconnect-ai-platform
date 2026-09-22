from pydantic import BaseModel


class FreelancerResult(BaseModel):
    id: int
    name: str
    service: str
    location: str
    phone: str | None
    verified: bool
    available: bool


class FreelancerSearchResponse(BaseModel):
    message: str
    freelancers: list[FreelancerResult]