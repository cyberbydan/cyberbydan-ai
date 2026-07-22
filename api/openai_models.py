"""
openai_models.py

OpenAI-compatible request and response models for the API

These models allow Open WebUI (and any OpenAI compatible client)
to communicate with the CyberByDan AI backend.
"""
from typing import List
from pydantic import BaseModel

# ============================================================
# Request Models
# ============================================================
class Message(BaseModel):
    role: str
    content: str

class ChatCompleteRequest(BaseModel):
    model: str
    messages: List[Message]

# ===========================================================
# Response Models
# ==========================================================
class ResponseMessage(BaseModel):
    role: str
    content: str

class Choice(BaseModel):
    index: int
    message: ResponseMessage
    finish_reason: str = "stop"

class ChatCompletionResponse(BaseModel):
    id: str
    object: str = "chat.completion"
    choices: List[Choice]
    created: int
    model: str
    

