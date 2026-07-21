"""
ingest.py

Entry point for the AI Knowledge Pipeline

At this stage we only perform document discovery. Later, this script will orchestrate the entire pipeline
"""
from loaders import discover_documents
from reader import read_document
from chunker import chunk_document

def main():
    documents = discover_documents()

    print(f"\nFound {len(documents)} document(s):\n")

    for document in documents:
        document = read_document(document)
        document = chunk_document(document)

        print("-" * 60)
        print(f"Source      : {document.source}")
        print(f"File        : {document.path.name}")
        print(f"Extension   : {document.extension}")
        print(f"Chunks      : {len(document.chunks)}")

        if document.chunks:
            first = document.chunks[0]
            print(f"Section     : {first.section}")
            print(f"Preview     : {first.content[:120].replace(chr(10), ' ')}...")

        else:
            print("Preview     : (No content loaded)")

if __name__ == "__main__":
    main()
