"""
chat.py
-------

Purpose
-------
This module orchestrates the complete Retrieval-Augmented Generation
(RAG) pipeline.

Unlike the other modules, this file performs very little work itself.

Instead, it coordinates the pipeline by calling each component in
the correct order.

Pipeline

User Question
      │
      ▼
Retrieve Relevant Chunks
      │
      ▼
Build Prompt
      │
      ▼
Ask DeepSeek
      │
      ▼
Return Answer
"""

from chat.retriever import retrieve
from chat.prompt import build_prompt
from chat.llm import ask_llm


# ============================================================
# Main Chat Function
# ============================================================

def chat(question: str) -> str:
    """
    Execute the complete RAG pipeline.

    Parameters
    ----------
    question : str
        The user's natural language question.

    Returns
    -------
    str
        The language model's answer.
    """

    # --------------------------------------------------------
    # Step 1
    # Retrieve the most relevant document chunks.
    # --------------------------------------------------------

    chunks = retrieve(question)

    # --------------------------------------------------------
    # Step 2
    # Build a prompt containing:
    #
    #   • System instructions
    #   • Retrieved context
    #   • User question
    # --------------------------------------------------------

    prompt = build_prompt(question, chunks)
    print("\n================ PROMPT ================\n")
    print(prompt)
    print("\n========================================\n")

    # --------------------------------------------------------
    # Step 3
    # Send the prompt to DeepSeek.
    # --------------------------------------------------------

    answer = ask_llm(prompt)

    return answer


# ============================================================
# Simple Command-Line Chat
#
# This allows us to test the complete pipeline without building
# the API or web interface yet.
# ============================================================

def main():

    print("=" * 60)
    print("CyberByDan AI")
    print("=" * 60)
    print()

    while True:

        question = input("You: ")

        if question.lower() in {
            "exit",
            "quit",
            "q",
        }:
            break

        print()

        answer = chat(question)

        print(answer)
        print()


if __name__ == "__main__":
    main()
