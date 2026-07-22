"""
routes.py

API endpoints
"""

from fastapi import APIRouter

from api.models import ChatRequest, ChatResponse
from chat.engine import chat

router = APIRouter()

@router.get("/")
def root():
    return {
        "message": "CyberByDan AI API"
    }

@router.get("/health")
def health():
    return {
        "status": "healthy"
    }

@router.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    """
    Endpoint for the CyberByDan AI chatbot
    """
    answer = chat(request.question)

    return ChatResponse(
        answer=answer,
        )
