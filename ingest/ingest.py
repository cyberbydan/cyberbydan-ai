"""
ingest.py

Entry point for the AI Knowledge Pipeline

Pipeline

Knowledge Folder
        │
        ▼
Discover Documents
        │
        ▼
Read Documents
        │
        ▼
Chunk Documents
        │
        ▼
Store in ChromaDB
"""

from loaders import discover_documents
from reader import read_document
from chunker import chunk_document
from vectorstore import store_chunks, count
# ============================================================

def main():
    """
    Runs the complete ingestion pipeline.
    """
    documents = discover_documents()

    print(f"\nFound {len(documents)} document(s):\n")

    # --------------------------------------------------------
    # This list will eventually contain EVERY chunk from
    # every document.
    #
    # Later we'll send the entire list to ChromaDB in one go.
    # --------------------------------------------------------

    all_chunks = []

    #--------------------------------------------------------
    # Process each document
    #--------------------------------------------------------

    for document in documents:
        document = read_document(document)
        document = chunk_document(document)
        # Add this document's chunks to the master list of all chunks.
        all_chunks.extend(document.chunks)

        # Print progress
        print("-" * 60)
        print(f"Source      : {document.source}")
        print(f"File        : {document.path.name}")
        print(f"Extension   : {document.extension}")
        print(f"Chunks      : {len(document.chunks)}")

        if document.chunks:
            first = document.chunks[0]

            print(f"Section     : {first.section}")
            print(
                f"Preview     : "
                f"{first.content[:120].replace(chr(10), ' ')}..."
            )

        else:
            print("Preview     : (No content loaded)")

    # --------------------------------------------------------
    # Store all chunks in ChromaDB
    # --------------------------------------------------------
    print("\nStoring embeddings...")
    store_chunks(all_chunks)
    print(f"\nVector database now contains {count()} chunks.\n")

if __name__ == "__main__":
    main()
