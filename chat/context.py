"""
context.py
----------

Purpose
-------
Builds a structured context block from retrieved chunks.

The retriever finds the most relevant information.

This module prepares that information for the language model
by presenting it in a consistent, readable format.

Pipeline

Retrieved Chunks
        │
        ▼
Context Builder
        │
        ▼
Formatted Context
        │
        ▼
Language Model
"""

from typing import List


# ============================================================
# Build Context
# ============================================================

def build_context(chunks: List[dict]) -> str:
    """
    Convert retrieved chunks into a structured context block
    for the language model.

    Parameters
    ----------
    chunks
        List of retrieved chunks from ChromaDB.

    Returns
    -------
    str

        A formatted block of documentation ready to be inserted
        into the prompt.
    """

    if not chunks:
        return (
            "No relevant documentation was found for this question."
        )

    sections = []

    for index, chunk in enumerate(chunks, start=1):

        section = [
            "=" * 60,
            f"Evidence {index}",
            "",
            f"Source: {chunk['source']}",
            f"Document: {chunk['document']}",
            f"Section: {chunk['section']}",
            f"Similarity: {chunk['similarity']:.3f}",
            "",
            "Content:",
            chunk["content"].strip(),
        ]

        sections.append("\n".join(section))

    return "\n\n".join(sections)


# ============================================================
# Preview (Development Only)
# ============================================================

if __name__ == "__main__":

    sample = [
        {
            "source": "Homelab",
            "document": "homelab_architecture_v5.md",
            "section": "Networking",
            "similarity": 0.947,
            "content": (
                "The homelab uses Docker, Tailscale, "
                "and Homepage as its primary dashboard."
            ),
        }
    ]

    print(build_context(sample))
