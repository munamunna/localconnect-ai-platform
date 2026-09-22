from app.llm.ollama_llm import generate_structured_response
from app.schemas.agent import FreelancerSearchRequest


def extract_freelancer_search_parameters(
    query: str,
) -> FreelancerSearchRequest:
    if not query or not query.strip():
        raise ValueError("Query is required")

    system_prompt = """
You extract freelancer search parameters for LocalConnect.

Extract:
- service: the type of freelancer/service the customer needs
- location: the location where the customer needs the service

Rules:
- Return only the requested structured fields.
- Do not invent missing information.
- Preserve the customer's intended service and location.
"""

    content = generate_structured_response(
        system_prompt=system_prompt,
        user_message=query.strip(),
        output_schema=FreelancerSearchRequest.model_json_schema(),
    )

    return FreelancerSearchRequest.model_validate_json(content)