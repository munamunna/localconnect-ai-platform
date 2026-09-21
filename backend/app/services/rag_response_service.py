from app.llm.ollama_llm import generate_text_response
from app.services.rag_context_service import build_rag_context


def generate_rag_response(
    query: str,
    limit: int = 5,
) -> str:
    if not query or not query.strip():
        raise ValueError("Query is required")

    context = build_rag_context(
        query=query,
        limit=limit,
    )

    if not context:
        return "I don't have enough information to answer that."

    system_prompt = """
You are a helpful AI assistant for LocalConnect.

Answer the customer's question using the provided knowledge context.

Rules:
- Use the provided context as the primary source of information.
- Do not invent services, prices, availability, or other business information.
- If the context does not contain enough information, clearly say that you do not have enough information.
- Keep the response concise and useful.
"""

    user_message = f"""
Customer question:
{query.strip()}

Knowledge context:
{context}
"""

    return generate_text_response(
    system_prompt=system_prompt,
    user_message=user_message,
)