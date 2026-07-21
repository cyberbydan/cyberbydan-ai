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
# Knowledge directory
KNOWLEDGE_DIR = PROJECT_ROOT / "knowledge"
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
COLLECTION_NAME = "cyberbydan-knowledge"
