"""
config.py
---------

Central configuration for the AI platform.

This file contains every value that is expected to change
between environments (paths, models, chunk sizes, etc.).

The rest of the codebase should import from here instead of
hardcoding values.
"""

from pathlib import Path

# ==========================
# Project Directories
# ==========================

# Project root directory (C:\homelab\ai)
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# ===========================================================
# Knowledge Sources
# ===========================================================

# Every source listed here will be indexed into ChromaDB.
#
# CyberByDan AI consumes documentation but does not own it.
# The Homelab repository remains the single source of truth.
#
# Additional knowledge collections can be added here without
# changing the ingestion pipeline.

KNOWLEDGE_SOURCES = [
    {
        "name": "Homelab",
        "path": PROJECT_ROOT.parent / "docs",
        "enabled": True,
    }
]

# ===========================================================
# Retrieval Priorities
# ===========================================================

DOCUMENT_PRIORITIES = {

    # Core architecture
    "homelab_architecture_v5.md": 100,
    "state-inventory v2.md": 95,
    "recovery-playbooks.md": 90,
    "superbot-architecture.md": 85,

    # Historical documentation
    "lessons-learned.md": 70,

    # Session history
    "session-06.md": 40,
    "session-05.md": 35,
    "session-5-plan.md": 20,
}

# Maximum number of retrieved chunks allowed
# from the same document.
MAX_CHUNKS_PER_DOCUMENT = 2

# Chroma Persistence directory
CHROMA_DIR = PROJECT_ROOT / "chroma_db"

# Supported file types
SUPPORTED_EXTENSIONS = {
    ".md",
    ".txt",
    ".pdf",
    ".docx",
    ".json",
    ".yaml",
    ".yml",
    ".toml",
    ".ini",
    ".py",
    ".ps1",
    ".sh",
    ".log"
}

# ============================================================
# Chunking
# ============================================================

CHUNK_SIZE = 800

CHUNK_OVERLAP = 150

HEADERS_TO_SPLIT_ON = [
    ("#", "Header 1"),
    ("##", "Header 2"),
    ("###", "Header 3"),
    ("####", "Header 4"),
    ("#####", "Header 5"),
    ("######", "Header 6"),
]

# ============================================================
# Ollama
# ============================================================

OLLAMA_URL = "http://localhost:11434"

EMBEDDING_MODEL = "nomic-embed-text:latest"

CHAT_MODEL = "deepseek-r1:14b"

# ============================================================
# ChromaDB
# ============================================================

CHROMA_HOST = "localhost"
CHROMA_PORT = 8000
CHROMA_COLLECTION = "cyberbydan-knowledge"
