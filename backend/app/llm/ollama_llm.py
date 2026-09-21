import os

from ollama import chat


MODEL_NAME = os.getenv(
    "OLLAMA_MODEL",
    "llama3.2",
)


def generate_structured_response(
    system_prompt: str,
    user_message: str,
    output_schema: dict,
) -> str:

    response = chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_message,
            },
        ],
        format=output_schema,
    )

    return response.message.content


def generate_text_response(
    system_prompt: str,
    user_message: str,
) -> str:
    response = chat(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
    )

    return response.message.content