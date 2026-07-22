"""
app.py

Creates the FastAPI application
"""

from fastapi import FastAPI
from api.routes import router

app = FastAPI(
    title="CyberByDan AI",
    version="0.1.0",
    description="Local Retrieval-Augmented Generation API"
)

app.include_router(router)
