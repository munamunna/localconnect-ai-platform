from ollama import embed


EMBEDDING_MODEL = "nomic-embed-text"


def generate_embedding(text: str) -> list[float]:
    if not text or not text.strip():
        raise ValueError("Text is required")

    response = embed(
        model=EMBEDDING_MODEL,
        input=text.strip(),
    )

    return response["embeddings"][0]