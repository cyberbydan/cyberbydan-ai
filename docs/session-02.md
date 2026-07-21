# Session 02 – Building the Knowledge Pipeline

## Objective
Build the complete document ingestion pipeline for the local AI platform.

## Completed

- Implemented Document model
- Implemented Chunk model
- Markdown-aware chunking using LangChain
- Recursive chunk splitting
- Metadata extraction from Markdown headings
- Ollama embedding integration
- Batch embedding support
- ChromaDB container integration
- HTTP client communication with ChromaDB
- End-to-end ingestion pipeline

## Statistics

Documents processed: 10

Chunks generated: 273

Embedding model:
nomic-embed-text

Vector database:
ChromaDB

Collection:
cyberbydan-knowledge

## Lessons Learned

- Separate responsibilities into dedicated modules.
- The Chunk object is the central data model.
- Batch embeddings are much more efficient than individual requests.
- Metadata greatly improves retrieval quality.
- Treat ChromaDB as an independent infrastructure service rather than a local library.
