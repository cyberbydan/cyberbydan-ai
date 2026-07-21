"""
embedder.py
-----------

This module is responsible for converting text into semantic vectors
(embeddings) using Ollama.

Why does this module exist?

We don't want the rest of the application worrying about
how embeddings are generated.

Instead, every other module simply asks:

"Give me an embedding for this text." or "Give me embeddings for these texts."

If we ever change embedding models (for example from nomic-embed-text to BGE-M3), this is the ONLY file that should need changing.
"""

from ollama import Client

from config import (
    EMBEDDING_MODEL,
    OLLAMA_URL,
)

# ============================================================
# Create a reusable connection to Ollama.
#
# The Ollama server is already running in the background.
# This client simply communicates with it over HTTP.

# ============================================================
client = Client(host=OLLAMA_URL)
# ============================================================

# Single Embedding
# ============================================================
def create_embedding(text: str) -> list[float]:
    """
    Create an embedding for a single piece of text.

    This is primarily used during SEARCH.

    Example:

        User asks:
        "How are backups handled?"

        That single question becomes one embedding which can then be compared against every stored document.
    """

    response = client.embed(
        model=EMBEDDING_MODEL,
        input=text,
    )

    return response["embeddings"][0]


# ============================================================
# Batch Embeddings
# ============================================================

def create_embeddings(texts: list[str]) -> list[list[float]]:
    """
    Create embeddings for multiple pieces of text.

    This is primarily used during INGESTION.

    Instead of making hundreds of separate requests to Ollama, we send every chunk in a single request.

    Example:

        README chunk 1
        README chunk 2
        README chunk 3
        Lessons chunk 1
        Lessons chunk 2

                ↓

        Ollama

                ↓

        [
            embedding_1,
            embedding_2,
            embedding_3,
            embedding_4,
            embedding_5
        ]
    """

    response = client.embed(
        model=EMBEDDING_MODEL,
        input=texts,
    )

    return response["embeddings"]
