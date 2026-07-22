"""
prompt.py
---------

Purpose
-------
Builds the final prompt that will be sent to the language model.

The prompt combines:

    • System instructions
    • Retrieved knowledge
    • User question

The language model never talks directly to ChromaDB.

Instead it receives a carefully constructed prompt generated
by this module.
"""

# ============================================================
# System Prompt
# ============================================================

SYSTEM_PROMPT = """
You are CyberByDan AI.

You are an expert assistant for Dan Isaaka's homelab,
documentation and technical projects.

Your responsibilities are:

- Answer questions using ONLY the supplied context.
- Be technically accurate.
- Explain concepts clearly.
- If the answer is not present in the context,
  say you do not know.
- Never invent commands, paths or configuration.
- When appropriate, explain your reasoning step-by-step.
"""

# ============================================================
# Prompt Builder
# ============================================================

def build_prompt(
    question: str,
    chunks: list[dict],
) -> str:
    """
    Builds the complete prompt for the LLM.

    Parameters
    ----------
    question
        User's question.

    chunks
        Relevant chunks returned from the retriever.

    Returns
    -------
    str

        Complete prompt ready for DeepSeek.
    """

    # --------------------------------------------------------
    # Build the context section.
    # --------------------------------------------------------

    context = ""

    for chunk in chunks:

        context += f"""
Document : {chunk["document"]}
Section  : {chunk["section"]}

{chunk["content"]}

------------------------------------------------------------
"""

    # --------------------------------------------------------
    # Assemble the final prompt.
    # --------------------------------------------------------

    prompt = f"""
{SYSTEM_PROMPT}

============================================================
CONTEXT
============================================================

{context}

============================================================
QUESTION
============================================================

{question}

============================================================
ANSWER
============================================================
"""

    return prompt.strip()
