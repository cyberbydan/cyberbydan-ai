"""
models.py

Purpose
-------
Defines the core data models used throughout the AI Knowledge Pipeline.

Pipeline

Knowledge Folder
        │
        ▼
Document Discovery
        │
        ▼
Document Model
        │
        ▼
Chunk Model
        │
        ▼
Embeddings
        │
        ▼
ChromaDB
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

#---------------------------------------------------------------------
# DOCUMENT
#---------------------------------------------------------------------

@dataclass
class Document:
    """
    Represents one source document before processing.

    As the pipeline progresses, this object gains more information.
    """

    # Full path to the file on disk
    path: Path

    # Top-level knowledge collection.
    # Examples: homelab, cisa, linux
    source: str

    # File extension.
    extension: str

    # Raw text extracted from the file.
    content: Optional[str] = None

    # Chunks derived from the document.
    # Starts empty and is populated later in the pipeline.
    chunks: list["Chunk"] = field(default_factory=list)

# ---------------------------------------------------------------------
# CHUNK
# ---------------------------------------------------------------------
@dataclass
class Chunk:
    """
    Represents a chunk of text derived from a Document. Chunks are what eventually receive embeddings and are stored in ChromaDB.
    """

    # Parent document
    document: Document
    # Chunk position within the document
    chunk_number: int
    # Markdown section heading (if any)
    section: str
    # The actual text that will be embedded
    content: str
    # Additional metadata we'll store alongside the embedding
    metadata: dict = field(default_factory=dict)
