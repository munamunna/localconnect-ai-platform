from unittest.mock import patch

import pytest

from app.services.embedding_service import generate_embedding


def test_generate_embedding_success():
    fake_embedding = [0.1] * 768

    with patch(
        "app.services.embedding_service.embed",
        return_value={
            "embeddings": [fake_embedding],
        },
    ) as mock_embed:

        result = generate_embedding(
            "Plumbing services include pipe repair."
        )

    assert result == fake_embedding
    assert len(result) == 768

    mock_embed.assert_called_once_with(
        model="nomic-embed-text",
        input="Plumbing services include pipe repair.",
    )


def test_generate_embedding_strips_whitespace():
    fake_embedding = [0.1] * 768

    with patch(
        "app.services.embedding_service.embed",
        return_value={
            "embeddings": [fake_embedding],
        },
    ) as mock_embed:

        result = generate_embedding(
            "  Plumbing services  "
        )

    assert result == fake_embedding

    mock_embed.assert_called_once_with(
        model="nomic-embed-text",
        input="Plumbing services",
    )


def test_generate_embedding_requires_text():
    with pytest.raises(
        ValueError,
        match="Text is required",
    ):
        generate_embedding("")


def test_generate_embedding_rejects_whitespace():
    with pytest.raises(
        ValueError,
        match="Text is required",
    ):
        generate_embedding("   ")