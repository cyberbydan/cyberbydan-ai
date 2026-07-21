from pathlib import Path

# Project root directory (C:\homelab\ai)
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Knowledge directory
KNOWLEDGE_DIR = PROJECT_ROOT / "knowledge"

# Chroma Persistence directory
CHROMA_DIR = PROJECT_ROOT / "chroma_db"

# Supported file types
SUPPORTED_EXTENSIONS = {
    ".txt",
    ".pdf",
    ".docx",
    ".pptx",
    ".md",
    ".csv",
}
