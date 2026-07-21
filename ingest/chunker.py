"""
chunker.py

Purpose
-------
This module is responsible for splitting documents into smaller,
searchable pieces called "chunks".

Why do we chunk documents?
--------------------------
Large Language Models (LLMs) and embedding models perform much better
when they work with small, focused pieces of text instead of an
entire document.

Instead of embedding one huge README file, we split it into many
smaller chunks.

Example:

README.md
    │
    ▼
+---------------------------+
| Introduction              |
+---------------------------+

+---------------------------+
| Infrastructure            |
+---------------------------+

+---------------------------+
| Backup Strategy           |
+---------------------------+

Each chunk will later receive its own embedding and be stored
inside ChromaDB.

Pipeline
--------
Knowledge Folder
        │
        ▼
Discover Documents
        │
        ▼
Read Documents
        │
        ▼
Chunk Documents   <-- This module
        │
        ▼
Generate Embeddings
        │
        ▼
Store in ChromaDB
"""
def get_section_name(metadata: dict) -> str:
    """
    Returns the deepest Markdown heading available.

    LangChain stores headings inside metadata using keys such as:
        Header 1
        Header 2
        ...
        Header 6

    We search from the deepest heading upward so that a subsection
    title is preferred over its parent section.

    If no heading exists, we return 'Untitled'.
    """

    # Search from Header 6 back to Header 1.
    for level in range(6, 0, -1):
        key = f"Header {level}"

        if key in metadata:
            return metadata[key]

    return "Untitled"

from langchain_text_splitters import(
    MarkdownHeaderTextSplitter,
    RecursiveCharacterTextSplitter,
)

from models import Document, Chunk


#---------------------------------------------------------------------
# Chunking Configuration
#---------------------------------------------------------------------

# Preserve Markdown structure by splitting on headings first.
HEADERS_TO_SPLIT_ON = [
    ("#", "Header 1"),
    ("##", "Header 2"),
    ("###", "Header 3"),
    ("####", "Header 4"),
    ("#####", "Header 5"),
    ("######", "Header 6"),
]

# Maximum number of characters in each chunk.
CHUNK_SIZE = 800

# Number of characters shared between neighbouring chunks.
# This helps preserve context across chunk boundaries.
CHUNK_OVERLAP = 150

#---------------------------------------------------------------------
# LangChain Splitters
#--------------------------------------------------------------------

# First splitter:
# Keeps Markdown sections together.
markdown_splitter = MarkdownHeaderTextSplitter(
    headers_to_split_on=HEADERS_TO_SPLIT_ON,
    strip_headers=False,
)

# Second splitter:
# Breaks large sections into smaller overlapping chunks.
recursive_splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP,
)

#---------------------------------------------------------------------
# Chunking Function
#---------------------------------------------------------------------

def chunk_document(document: Document) -> Document:
    """
    Splits a Document into smaller Chunk objects.

    Parameters
    ----------
    document : Document
        A document whose content has already been loaded.

    Returns
    -------
    Document

        The SAME Document object.

        The only difference is that the document's "chunks"
        list is now populated.
    """

    # Safety check.
    # If there is no content, there is nothing to split.
    if not document.content:
        return document

    # Step 1:
    # Split the document into Markdown sections.
    markdown_sections = markdown_splitter.split_text(document.content)

    # Keep track of chunk numbering.
    chunk_number = 1

    # Step through every Markdown section.
    for section in markdown_sections:

        # Retrieve the section heading.
        #
        # LangChain stores heading information inside metadata.
        section_name = get_section_name(section.metadata)

        # Step 2:
        # Split the section into smaller chunks.
        text_chunks = recursive_splitter.split_text(section.page_content)

        # Convert every text chunk into our own Chunk model.
        for text in text_chunks:

            chunk = Chunk(
                id=f"{document.stem}::{chunk_number:04}",
                document=document,
                chunk_number=chunk_number,
                section=section_name,
                content=text,
                metadata=section.metadata,
            )

            # Attach the chunk to the document.
            document.chunks.append(chunk)

            chunk_number += 1

    return document
