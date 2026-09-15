from pydantic import BaseModel


from datetime import datetime

from pydantic import BaseModel


class FreelancerCreate(BaseModel):

    name: str

    service: str

    location: str

    phone: str | None = None

    verified: bool = False

    available: bool = True


class FreelancerResponse(BaseModel):

    id: int

    name: str

    service: str

    location: str

    phone: str | None = None

    verified: bool

    available: bool

    created_at: datetime | None = None


class FreelancerMatchRequest(BaseModel):

    service: str

    location: str


class FreelancerMatchResponse(BaseModel):

    matches: list[FreelancerResponse]