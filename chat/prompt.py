"""
prompt.py
---------

Purpose
-------
Builds the final prompt sent to the language model.

The prompt combines:

    • System instructions
    • Retrieved documentation
    • User question

The language model never communicates directly with ChromaDB.

Instead it receives carefully structured context prepared by
the Context Builder.
"""

# ============================================================
# System Prompt
# ============================================================

SYSTEM_PROMPT = """
You are CyberByDan AI.

You are the AI assistant for Dan Isaaka's homelab, software
projects and technical documentation.

Your goals are:

• Answer ONLY using the supplied documentation.

• If the documentation does not contain enough information,
  clearly say so.

• Never invent commands, file paths, configuration values,
  services or architecture.

• Combine information from multiple pieces of documentation
  whenever appropriate.

• Prefer complete explanations over short answers.

• Explain technical concepts clearly and logically.

• Do not mention internal similarity scores or retrieval
  mechanics.

• Treat the supplied documentation as evidence supporting
  your answer, not as text to copy verbatim.

• If documentation conflicts, prefer architecture documents
  over session notes.

Your job is to produce accurate, grounded technical answers.
"""

# ============================================================
# Prompt Builder
# ============================================================

def build_prompt(
    question: str,
    context: str,
) -> str:
    """
    Build the final prompt sent to the language model.

    Parameters
    ----------
    question
        User's question.

    context
        Formatted documentation produced by the
        Context Builder.

    Returns
    -------
    str
        Complete prompt ready for the language model.
    """

    return f"""
{SYSTEM_PROMPT}

============================================================
RETRIEVED DOCUMENTATION
============================================================

{context}

============================================================
USER QUESTION
============================================================

{question}

============================================================
ANSWER
============================================================

Answer using the retrieved documentation above.
If the documentation is incomplete, explicitly state that.
""".strip()
