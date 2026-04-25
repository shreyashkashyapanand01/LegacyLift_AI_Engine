import google.generativeai as genai
from .base_provider import BaseLLMProvider
from parsing.rag.llm.config import GEMINI_API_KEY, LLM_MODEL


class GeminiProvider(BaseLLMProvider):

    def __init__(self):
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel(LLM_MODEL)

    def generate(self, prompt: str) -> str:
        response = self.model.generate_content(prompt)
        return response.text