""""
models.py

Request and response models for the API"""

from pydantic import BaseModel

class ChatRequest(BaseModel):
    question: str
    
class ChatResponse(BaseModel):
    answer: str
