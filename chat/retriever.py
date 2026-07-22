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

collection = client.get_collection(CHROMA_COLLECTION)


# ============================================================
# Retrieve Similar Chunks
# ============================================================

def retrieve(question: str, n_results: int = 5) -> list[dict]:
    """
    Search the vector database for chunks relevant to the question.

    Parameters
    ----------
    question
        The user's natural language question.

    n_results
        Maximum number of chunks to return.

    Returns
    -------
    list[dict]

        Each dictionary contains information about one retrieved
        chunk.
    """

    # --------------------------------------------------------
    # Step 1
    # Convert the question into an embedding.
    # --------------------------------------------------------

    query_embedding = create_embedding(question)

    # --------------------------------------------------------
    # Step 2
    # Search ChromaDB.
    # --------------------------------------------------------

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
    )

    # --------------------------------------------------------
    # Step 3
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
                "distance": distance,
                "metadata": metadata,
            }
        )

    return retrieved_chunks
