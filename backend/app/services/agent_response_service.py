from app.schemas.agent_response import (
    FreelancerResult,
    FreelancerSearchResponse,
)


def format_freelancer_search_response(
    results: list[tuple],
) -> FreelancerSearchResponse:
    freelancers = []

    for result in results:
        freelancer = FreelancerResult(
            id=result[0],
            name=result[1],
            service=result[2],
            location=result[3],
            phone=result[4],
            verified=result[5],
            available=result[6],
        )

        freelancers.append(freelancer)

    if not freelancers:
        return FreelancerSearchResponse(
            message="No matching freelancers were found.",
            freelancers=[],
        )

    count = len(freelancers)

    message = (
        f"I found {count} freelancer"
        f"{'s' if count != 1 else ''} matching your request."
    )

    return FreelancerSearchResponse(
        message=message,
        freelancers=freelancers,
    )