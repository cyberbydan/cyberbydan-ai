"""
vectorstore.py

Purpose
-------
Provides a simple interface for storing and retrieving semantic
knowledge using ChromaDB.

Pipeline

Chunk Objects
        │
        ▼
Generate Embeddings
        │
        ▼
Store in ChromaDB
        │
        ▼
Similarity Search
        │
        ▼
Return Matching Chunks

This module ONLY communicates with ChromaDB.

It does NOT:

- Read files
- Chunk documents
- Talk to DeepSeek

Its only responsibility is vector storage and retrieval.
"""

from chromadb import HttpClient

from core.config import (
    CHROMA_HOST,
    CHROMA_PORT,
    CHROMA_COLLECTION,
)

from ai.core.embedder import create_embedding, create_embeddings
from ai.core.models import Chunk


# ============================================================
# Connect to ChromaDB
# ============================================================

client = HttpClient(
    host=CHROMA_HOST,
    port=CHROMA_PORT,
)

# ============================================================
# Create (or load) our collection
# ============================================================

collection = client.get_or_create_collection(
    name=CHROMA_COLLECTION
)


# ============================================================
# Store Chunks
# ============================================================

def store_chunks(chunks: list[Chunk]) -> None:
    """
    Stores a list of Chunk objects inside ChromaDB.

    Workflow

        Chunks
            │
            ▼
    Generate embeddings
            │
            ▼
    Attach embeddings to Chunk objects
            │
            ▼
    Save everything to ChromaDB
    """

    if not chunks:
        print("No chunks to store.")
        return

    # --------------------------------------------------------
    # Extract raw text from every chunk.
    # --------------------------------------------------------

    texts = [chunk.content for chunk in chunks]

    # --------------------------------------------------------
    # Generate embeddings in one request.
    # --------------------------------------------------------

    embeddings = create_embeddings(texts)

    # --------------------------------------------------------
    # Attach embeddings back to each Chunk.
    # --------------------------------------------------------

    for chunk, embedding in zip(chunks, embeddings):
        chunk.embedding = embedding

    # --------------------------------------------------------
    # Save everything.
    # --------------------------------------------------------

    collection.add(
        ids=[
            chunk.id
            for chunk in chunks
        ],

        documents=[
            chunk.content
            for chunk in chunks
        ],

        embeddings=[
            chunk.embedding
            for chunk in chunks
        ],

        metadatas=[
            {
                "source": chunk.document.source,
                "filename": chunk.filename,
                "section": chunk.section,
                "chunk_number": chunk.chunk_number,
                **chunk.metadata,
            }
            for chunk in chunks
        ],
    )

    print(f"Stored {len(chunks)} chunks.")


# ============================================================
# Search
# ============================================================

def search(
    query: str,
    n_results: int = 5,
):
    """
    Performs semantic similarity search.

    Example

        "How are backups performed?"

    becomes

        embedding

    which is compared against every stored document.
    """

    query_embedding = create_embedding(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
    )

    return results


# ============================================================
# Collection Information
# ============================================================

def count() -> int:
    """
    Returns the number of stored chunks.
    """

    return collection.count()


# ============================================================
# Delete Everything
# ============================================================

def clear() -> None:
    """
    Deletes every stored embedding.

    Useful while developing.
    """

    global collection

    client.delete_collection(CHROMA_COLLECTION)

    collection = client.get_or_create_collection(
        name=CHROMA_COLLECTION
    )

    print("Collection cleared.")
