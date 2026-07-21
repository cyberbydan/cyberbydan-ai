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
from typing import Any, Optional


# ============================================================
# DOCUMENT
# ============================================================

@dataclass
class Document:
    """
    Represents a single source document before processing.

    A Document starts as simply a file on disk.

    As it moves through the pipeline it gains:

    - raw content
    - semantic chunks

    The Document itself is NEVER embedded.

    Only its chunks are embedded.
    """

    # --------------------------------------------------------
    # Full path to the file on disk.
    # Example:
    #
    # C:/homelab/ai/knowledge/homelab/README.md
    # --------------------------------------------------------

    path: Path

    # --------------------------------------------------------
    # Top-level knowledge collection.
    #
    # Examples
    #
    # homelab
    # linux
    # cisa
    # python
    # --------------------------------------------------------

    source: str

    # File extension
    extension: str

    # Entire document text
    content: Optional[str] = None

    # All chunks generated from this document
    chunks: list["Chunk"] = field(default_factory=list)

    # --------------------------------------------------------
    # Convenience Properties
    # --------------------------------------------------------

    @property
    def filename(self) -> str:
        """
        Returns:

        README.md
        """

        return self.path.name

    @property
    def stem(self) -> str:
        """
        Returns:

        README
        """

        return self.path.stem


# ============================================================
# CHUNK
# ============================================================

@dataclass
class Chunk:
    """
    Represents one semantic chunk extracted from a document.

    This is the primary object used throughout the AI platform.

    A Chunk eventually gains:

        Text
            ↓
        Embedding
            ↓
        ChromaDB storage
            ↓
        Retrieval
            ↓
        DeepSeek context
    """

    # --------------------------------------------------------
    # Stable unique identifier.
    #
    # Example:
    #
    # README::0001
    # README::0002
    # README::0003
    # --------------------------------------------------------

    id: str

    # Parent document
    document: Document

    # Position within the document
    chunk_number: int

    # Markdown heading
    section: str

    # Text to embed
    content: str

    # Semantic embedding
    #
    # Initially None.
    # Populated after embedder.py runs.
    embedding: Optional[list[float]] = None

    # Additional metadata stored in ChromaDB.
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def filename(self) -> str:
        """
        Shortcut to the parent document filename.

        Instead of writing:

            chunk.document.filename

        we can simply write:

            chunk.filename
        """

        return self.document.filename
