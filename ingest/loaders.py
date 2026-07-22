"""
loaders.py

Purpose
-------
This module discovers documents from one or more configured
knowledge sources.

It does NOT read document contents.

Its only responsibility is to locate supported files and
convert them into Document objects.

Pipeline

Knowledge Sources
        │
        ▼
Discover Files
        │
        ▼
Document Objects
"""

from core.config import KNOWLEDGE_SOURCES, SUPPORTED_EXTENSIONS
from core.models import Document


def discover_documents():
    """
    Search every enabled knowledge source for supported files.

    Returns
    -------
    list[Document]
        Each discovered file becomes a Document object.
    """

    documents = []

    # --------------------------------------------------------
    # Search every enabled knowledge source
    # --------------------------------------------------------

    for source in KNOWLEDGE_SOURCES:

        if not source.get("enabled", True):
            continue

        source_name = source["name"]
        source_path = source["path"]

        # Skip sources that do not exist
        if not source_path.exists():
            print(f"Warning: Knowledge source not found: {source_path}")
            continue

        # Search every file recursively
        for path in source_path.rglob("*"):

            # Skip folders
            if not path.is_file():
                continue

            # Skip unsupported file types
            if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
                continue

            document = Document(
                path=path,
                source=source_name,
                extension=path.suffix.lower(),
            )

            documents.append(document)

    return sorted(documents, key=lambda doc: str(doc.path))
