"""
retriever.py
------------

Purpose
-------
Searches the ChromaDB vector database for the document chunks
most relevant to a user's question.

The retriever DOES NOT answer questions.

Its only responsibility is to:

    Question
        │
        ▼
    Create embedding
        │
        ▼
    Search ChromaDB
        │
        ▼
    Return the best matching chunks

Those chunks will later be used by the prompt builder.
"""

from chromadb import HttpClient

from core.embedder import create_embedding
from core.config import (
    CHROMA_COLLECTION,
    CHROMA_HOST,
    CHROMA_PORT,
)


# ============================================================
# Connect to ChromaDB
# ============================================================

client = HttpClient(
    host=CHROMA_HOST,
    port=CHROMA_PORT,
)


# ============================================================
# Retrieve Similar Chunks
# ============================================================

def retrieve(question: str, n_results: int = 10) -> list[dict]:
    """
    Search the vector database for chunks relevant to the question.

    Parameters
    ----------
    question
        The user's natural language question.

    n_results
        Maximum number of chunks to retrieve before reranking.

    Returns
    -------
    list[dict]
        Retrieved chunks ordered by semantic similarity.
    """

    # --------------------------------------------------------
    # Step 1
    # Convert the question into an embedding.
    # --------------------------------------------------------

    query_embedding = create_embedding(question)

    # --------------------------------------------------------
    # Step 2
    # Get the latest collection.
    #
    # Using get_or_create_collection prevents stale collection
    # handles after rebuilding the vector database.
    # --------------------------------------------------------

    collection = client.get_or_create_collection(
        name=CHROMA_COLLECTION
    )

    # --------------------------------------------------------
    # Step 3
    # Search ChromaDB.
    # --------------------------------------------------------

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
    )

    # --------------------------------------------------------
    # Step 4
    # Convert Chroma's response into a cleaner Python object.
    # --------------------------------------------------------

    retrieved_chunks = []

    ids = results["ids"][0]
    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    for chunk_id, document, metadata, distance in zip(
        ids,
        documents,
        metadatas,
        distances,
    ):

        retrieved_chunks.append(
            {
                "id": chunk_id,
                "document": metadata.get("filename", "Unknown"),
                "section": metadata.get("section", "Unknown"),
                "source": metadata.get("source", "Unknown"),
                "content": document,

                # Lower distance means a better semantic match.
                "distance": round(distance, 4),

                # Higher similarity means a better match.
                "similarity": round(1 - distance, 4),

                "metadata": metadata,
            }
        )

    return retrieved_chunks
