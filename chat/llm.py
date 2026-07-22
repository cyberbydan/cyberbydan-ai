"""
llm.py
------

Purpose
-------
Provides a simple interface for communicating with the language model.

This module does NOT know:

- how documents are retrieved
- how prompts are built
- how ChromaDB works

It simply receives a finished prompt and asks the model to
generate a response.

Pipeline

Prompt
    │
    ▼
DeepSeek-R1 (Ollama)
    │
    ▼
Response
"""

from ollama import Client

from core.config import (
    CHAT_MODEL,
    OLLAMA_URL,
)

# ============================================================
# Create a reusable Ollama client.
#
# This client is shared across every request instead of
# creating a new HTTP connection every time.
# ============================================================

client = Client(host=OLLAMA_URL)


# ============================================================
# Ask the Language Model
# ============================================================

def generate(prompt: str) -> str:
    """
    Sends a prompt to the language model and returns its reply.

    Parameters
    ----------
    prompt : str
        A fully constructed prompt containing:
            - System instructions
            - Retrieved context
            - User question

    Returns
    -------
    str
        The model's response.
    """

    response = client.chat(
        model=CHAT_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    return response["message"]["content"]
