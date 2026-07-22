"""
app.py

Creates the FastAPI application
"""

from fastapi import FastAPI
from core.config import CHAT_MODEL

from api.routes import router
from api.openai_routes import router as openai_router

app = FastAPI(
    title="CyberByDan AI",
    version="0.1.0",
    description="Local Retrieval-Augmented Generation API"
)

# Existing API
app.include_router(router)

# OpenAI-compatible API
app.include_router(openai_router)
