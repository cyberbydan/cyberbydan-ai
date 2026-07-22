"""
reranker.py
-----------

Purpose
-------
Improves retrieval quality before context construction.

Responsibilities

• Prefer authoritative documentation.

• Prevent one document from dominating retrieval.

• Sort chunks into the best order for the LLM.
"""

from collections import defaultdict

from core.config import (
    DOCUMENT_PRIORITIES,
    MAX_CHUNKS_PER_DOCUMENT,
)


def rerank(chunks: list[dict]) -> list[dict]:
    """
    Improve retrieval ordering.

    Parameters
    ----------
    chunks
        Retrieved chunks.

    Returns
    -------
    list[dict]
        Better ordered chunks.
    """

    # ------------------------------------------
    # Calculate final ranking score.
    # ------------------------------------------

    for chunk in chunks:

        priority = DOCUMENT_PRIORITIES.get(
            chunk["document"],
            50,
        )

        chunk["priority"] = priority

        chunk["score"] = (
            priority
            + chunk["similarity"]
        )

    # ------------------------------------------
    # Highest score first.
    # ------------------------------------------

    chunks.sort(
        key=lambda chunk: chunk["score"],
        reverse=True,
    )

    # ------------------------------------------
    # Prevent one document dominating.
    # ------------------------------------------

    document_counts = defaultdict(int)

    filtered = []

    for chunk in chunks:

        document = chunk["document"]

        if document_counts[document] >= MAX_CHUNKS_PER_DOCUMENT:
            continue

        filtered.append(chunk)

        document_counts[document] += 1

    return filtered
