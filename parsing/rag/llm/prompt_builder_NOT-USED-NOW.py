# def build_code_prompt(query: str, context: str) -> str:

#     return f"""
# You are a senior software engineer.

# Answer the question using the given code context.

# ### Question:
# {query}

# ### Code Context:
# {context}

# ### Instructions:
# - Explain clearly
# - Be concise
# - Use code references if needed

# ### Answer:
# """


def build_code_prompt(query: str, context: str) -> str:
    return f"""
You are a senior software engineer.

Answer the user query based ONLY on the given code context.

STRICT RULES:
- Output MUST be valid JSON
- Do NOT add extra text outside JSON
- Do NOT explain outside JSON

JSON FORMAT:
{{
  "explanation": "...",
  "code_reference": "...",
  "examples": ["..."]
}}

USER QUERY:
{query}

CODE CONTEXT:
{context}
"""