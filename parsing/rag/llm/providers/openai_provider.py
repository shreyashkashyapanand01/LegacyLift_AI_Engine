from openai import OpenAI
from .base_provider import BaseLLMProvider
from parsing.rag.llm.config import OPENAI_API_KEY, LLM_MODEL


class OpenAIProvider(BaseLLMProvider):

    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)

    def generate(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=LLM_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )
        return response.choices[0].message.content