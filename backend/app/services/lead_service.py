from app.llm.ollama_llm import generate_structured_response
from app.schemas.lead import LeadInformation
from app.database.lead_repository import create_lead


def extract_lead(message: str) -> LeadInformation:

    system_prompt = """
You are a lead extraction AI for LocalConnect.

Your job is to extract structured information from a customer's message.

Extract these fields:

- service
- location
- urgency
- problem
- budget
- customer_intent
- lead_priority

Rules:

1. Never invent information.
2. If a field is not available, return null.
3. Extract information directly stated by the customer.
4. You may infer simple information only when it is clearly implied.
5. service should contain the requested service.
6. location should contain the customer's location.
7. urgency should contain the requested timing.
8. problem should contain the customer's actual problem.
9. budget should contain the budget if mentioned.
10. customer_intent should describe what the customer wants.
11. lead_priority must be exactly one of:
   - high
   - medium
   - low

Examples:

Customer:
"I need an electrician in Kozhikode tomorrow. There is a wiring problem in my house."

Expected:
{
    "service": "electrician",
    "location": "Kozhikode",
    "urgency": "tomorrow",
    "problem": "wiring problem",
    "budget": null,
    "customer_intent": "service_request",
    "lead_priority": "high"
}
"""

    content = generate_structured_response(
        system_prompt=system_prompt,
        user_message=message,
        output_schema=LeadInformation.model_json_schema(),
    )

    return LeadInformation.model_validate_json(content)


def save_lead(lead: LeadInformation):
    if not lead.service and not lead.location:
        raise ValueError(
            "Cannot save lead without service or location"
        )

    return create_lead(
        service=lead.service,
        location=lead.location,
        urgency=lead.urgency,
        problem=lead.problem,
        budget=lead.budget,
        customer_intent=lead.customer_intent,
        lead_priority=lead.lead_priority,
    )