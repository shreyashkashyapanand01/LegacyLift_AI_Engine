from parsing.rag.llm.config import LLM_PROVIDER

from parsing.rag.llm.providers.openai_provider import OpenAIProvider
from parsing.rag.llm.providers.groq_provider import GroqProvider
from parsing.rag.llm.providers.gemini_provider import GeminiProvider


class LLMService:

    def __init__(self):
        self.provider = self._load_provider()

    def _load_provider(self):
        if LLM_PROVIDER == "openai":
            return OpenAIProvider()

        elif LLM_PROVIDER == "groq":
            return GroqProvider()

        elif LLM_PROVIDER == "gemini":
            return GeminiProvider()

        else:
            raise ValueError(f"Unsupported LLM provider: {LLM_PROVIDER}")

    def generate(self, prompt: str) -> str:
        return self.provider.generate(prompt)