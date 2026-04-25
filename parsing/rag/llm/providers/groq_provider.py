from groq import Groq
from .base_provider import BaseLLMProvider
from parsing.rag.llm.config import GROQ_API_KEY, LLM_MODEL


class GroqProvider(BaseLLMProvider):

    def __init__(self):
        self.client = Groq(api_key=GROQ_API_KEY)

    def generate(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=LLM_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )
        return response.choices[0].message.content