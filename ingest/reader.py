"""
reader.py

Purpose
-------
Reads the contents of a Document.

The loader discovers WHERE a document is.

The reader opens the document and loads its contents into memory.

Pipeline

Document Discovery
        │
        ▼
Document Object
        │
        ▼
Read Contents   <-- This module
        │
        ▼
Document with content
"""

from pathlib import Path
from models import Document

def read_document(document: Document) -> Document:
    """
    Reads the contents of a Document and returns a new Document object with the content loaded.

    Parameters
    ----------
    document : Document
        The Document object to read.

    Returns
    -------
    Document
        A new Document object with the content loaded.
    """

    # Markdown and text files
    if document.extension in {".md", ".txt"}:

        document.content = document.path.read_text(
            encoding="utf-8",
            errors="ignore"
        )
        return document

    # Unsupported file types for now
    document.content = ""

    return document

