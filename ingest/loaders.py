"""
loaders.py

Purpose
-------
This module is responsible for discovering documents inside the
knowledge directory.

It DOES NOT read file contents.

Its only responsibility is to locate supported files and convert
them into Document objects.

Pipeline

Knowledge Folder
        │
        ▼
Discover Files      <-- This module
        │
        ▼
Document Objects
        │
        ▼
Content Loader
"""

from pathlib import Path

from config import KNOWLEDGE_DIR, SUPPORTED_EXTENSIONS
from models import Document

def discover_documents():
    """
       Search the knowledge directory for supported files.

    Returns
    -------
    list[Document]
    Each discovered file becomes a Document object.

    Example

    README.md

        ↓

    Document(
        path=...,
        source="homelab",
        extension=".md"
    )"""

    documents = []

    # Search every folder inside the knowledge directory
    for path in KNOWLEDGE_DIR.rglob("*"):

         # Skip anything that isn't a supported file.
        if not path.is_file():
            continue

        if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue

        # Determine which knowledge collection
        # the document belongs to.
        #
        # Example:
        #
        # knowledge/
        #     homelab/
        #         README.md
        #
        # source = "homelab"
        relative_path = path.relative_to(KNOWLEDGE_DIR)

        source = relative_path.parts[0]

        # Create a Document object.
        document = Document(
            path=path,
            source=source,
            extension=path.suffix.lower()
        )

        documents.append(document)

    return sorted(documents, key=lambda doc: str(doc.path))

