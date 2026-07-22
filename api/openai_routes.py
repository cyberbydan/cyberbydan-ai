"""
openai_routes.py

OpenAI-compatible API endpoints.

These endpoints allow Open WebUI and other OpenAI-compatible
clients to communicate with CyberByDan AI.
"""

import uuid
import time

from fastapi import APIRouter
from core.config import CHAT_MODEL

from ollama import Client
from core.config import OLLAMA_URL

from api.openai_models import(
    ChatCompleteRequest,
    ChatCompletionResponse,
    Choice,
    ResponseMessage,
)

from chat.engine import chat

router = APIRouter()
client = Client(host=OLLAMA_URL)
# ============================================================

@router.get("/v1/models")
def list_models():
    # Ask Ollama for every installed model
    ollama_models = client.list()
    models = []

    # ---------------------------------------------------
    # Our RAG assistant comes first
    # ---------------------------------------------------

    models.append(
        {
            "id": "CyberByDan-AI",
            "object": "model",
            "owned_by": "CyberByDan",
        }
    )

    # ---------------------------------------------------
    # Add every Ollama model
    # ---------------------------------------------------

    for model in ollama_models["models"]:

        models.append(
            {
                "id": model["model"],
                "object": "model",
                "owned_by": "Ollama",
            }
        )

    return {
        "object": "list",
        "data": models,
    }

@router.post("/v1/chat/completions", response_model = ChatCompletionResponse)
def chat_completion(request: ChatCompleteRequest):
    """
    OpenAI Chat completion endpoint for the CyberByDan AI
    """
    # ================================================
    # Get the latest user message
    # ================================================
    question = request.messages[-1].content

    # ===============================================
    # Ask our existing engine
    # ===============================================
    answer = chat(question)

    # ==============================================
    # Return an OpenAI-compatible response
    # ==============================================
    return ChatCompletionResponse(
            id = str(uuid.uuid4()),
            created = int(time.time()),
            model= "CyberByDan-AI",
            choices=[
                Choice(
                    index=0,
                    message=ResponseMessage(
                        role="assistant",
                        content=answer,
                    ),
                )
            ],
        )

