# AI Platform Development Log

> Building a local-first AI platform from scratch. Every milestone is documented to capture not only *what* was built, but *why* it was built and what was learned along the way.

---

# Session 01 — Document Ingestion Pipeline

**Date:** 21 July 2026

## Objective

Build the first stage of a Retrieval-Augmented Generation (RAG) pipeline capable of discovering documentation, reading its contents, and converting it into structured chunks that can later be embedded into a vector database.

---

## What Was Built

### Project Foundation

Created the initial project structure to support future AI capabilities.

```
ai/
├── api/
├── chromadb/
├── docs/
├── ingest/
├── knowledge/
├── mcp/
├── memory/
└── prompts/
```

---

### Document Discovery

Implemented automatic discovery of supported documentation within the knowledge directory.

Current supported formats include:

* Markdown (.md)
* Text (.txt)

The ingestion pipeline can be easily extended to support additional document formats.

---

### Document Reader

Implemented document loading with metadata extraction.

Each document records:

* Source
* Filename
* File extension
* Full text content

This metadata will later allow retrieved answers to reference their original source.

---

### Data Models

Created strongly typed models representing:

* Document
* Chunk

This separates raw documents from the semantic chunks that will ultimately be indexed inside ChromaDB.

---

### Markdown-Aware Chunking

Implemented a two-stage chunking strategy.

#### Stage 1

Split Markdown files by headings.

This preserves the logical structure of technical documentation.

Instead of treating documentation as one large block of text, the system understands sections such as:

* Hardware
* Backup Architecture
* Lessons Learned
* Incidents

#### Stage 2

Large sections are recursively split into smaller chunks suitable for embedding while maintaining overlap between adjacent chunks.

This improves retrieval quality by preserving context across chunk boundaries.

---

## Current Pipeline

```
Knowledge Base
        │
        ▼
Discover Documents
        │
        ▼
Read Contents
        │
        ▼
Extract Metadata
        │
        ▼
Markdown Header Split
        │
        ▼
Recursive Chunk Split
        │
        ▼
Chunk Objects
```

---

## Current Status

The pipeline successfully:

* Discovers documentation
* Reads file contents
* Preserves metadata
* Preserves Markdown structure
* Produces semantic chunks ready for embedding

The project is now prepared for vectorisation.

---

## Lessons Learned

* Good retrieval begins with good document structure.
* Markdown headings provide valuable semantic context.
* Separating documents from chunks creates a cleaner architecture.
* Strong data models simplify future development.
* Building the pipeline incrementally makes debugging and testing significantly easier.

---

## Next Milestone

Implement semantic embeddings using the local `nomic-embed-text` model and store vectors inside ChromaDB.

This will mark the transition from a document processing pipeline into a fully searchable knowledge base.
