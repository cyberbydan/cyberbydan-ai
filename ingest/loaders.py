from pathlib import Path
from config import SUPPORTED_EXTENSIONS, KNOWLEDGE_DIR

def discover_documents():
    files = []
    for path in KNOWLEDGE_DIR.rglob("*"):
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS:
            files.append(path)

    return sorted(files)
