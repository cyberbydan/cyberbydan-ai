"""
retriever.py
------------

Purpose
-------
Searches the ChromaDB vector database for the document chunks
most relevant to a user's question.
"""

from chromadb import HttpClient

from core.embedder import create_embedding
from core.config import (
    CHROMA_COLLECTION,
    CHROMA_HOST,
    CHROMA_PORT,
)

# ============================================================
# Lazy Chroma Connection
# ============================================================

_client = None
_collection = None


def get_collection():
    """
    Lazily connect to ChromaDB.

    The connection is created only once, on the first query,
    instead of during module import.
    """

    global _client
    global _collection

    if _collection is None:

        _client = HttpClient(
            host=CHROMA_HOST,
            port=CHROMA_PORT,
        )

        _collection = _client.get_collection(
            CHROMA_COLLECTION
        )

    return _collection


# ============================================================
# Retrieve Similar Chunks
# ============================================================

def retrieve(question: str, n_results: int = 5) -> list[dict]:
    """
    Search the vector database for chunks relevant to the question.
    """

    collection = get_collection()

    # --------------------------------------------------------
    # Step 1
    # Create query embedding.
    # --------------------------------------------------------

    query_embedding = create_embedding(question)

    # --------------------------------------------------------
    # Step 2
    # Query Chroma.
    # --------------------------------------------------------

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
    )

    # --------------------------------------------------------
    # Step 3
    # Convert results.
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
                "distance": round(distance, 4),
                "similarity": round(1 - distance, 4),
                "metadata": metadata,
            }
        )

    return retrieved_chunks
