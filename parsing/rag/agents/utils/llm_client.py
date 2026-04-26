import os
import time
import logging
from typing import Optional
from parsing.rag.agents.config.settings import Settings

from dotenv import load_dotenv

# Providers
from openai import OpenAI
from groq import Groq
import google.generativeai as genai

logger = logging.getLogger(__name__)

load_dotenv()


class LLMClient:
    def __init__(self):
        # self.provider = os.getenv("LLM_PROVIDER", "openai").lower()
        # self.model = os.getenv("LLM_MODEL", "")
        self.provider = Settings.LLM_PROVIDER
        self.model = Settings.LLM_MODEL
        self.temperature = Settings.TEMPERATURE

        logger.info(f"LLM Provider: {self.provider} | Model: {self.model}")

        if self.provider == "openai":
            self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        elif self.provider == "groq":
            self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))

        elif self.provider == "gemini":
            genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
            self.client = genai.GenerativeModel(self.model)

        else:
            raise ValueError(f"Unsupported LLM provider: {self.provider}")

    # ---------------------------
    # 🔥 MAIN GENERATE FUNCTION
    # ---------------------------
    def generate(self, prompt: str, temperature: float = 0.2, max_tokens: int = 1000) -> str:
        """
        Unified generate function across providers
        """
        for attempt in range(3):  # retry mechanism
            try:
                if self.provider == "openai":
                    return self._openai_generate(prompt, temperature, max_tokens)

                elif self.provider == "groq":
                    return self._groq_generate(prompt, temperature, max_tokens)

                elif self.provider == "gemini":
                    return self._gemini_generate(prompt)

            except Exception as e:
                logger.warning(f"LLM attempt {attempt+1} failed: {e}")
                time.sleep(1)

        raise RuntimeError("LLM failed after retries")

    # ---------------------------
    # 🔹 OPENAI
    # ---------------------------
    def _openai_generate(self, prompt, temperature, max_tokens):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a strict JSON generator."},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature,
            max_tokens=max_tokens
        )

        return response.choices[0].message.content

    # ---------------------------
    # 🔹 GROQ
    # ---------------------------
    def _groq_generate(self, prompt, temperature, max_tokens):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a strict JSON generator."},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature,
            max_tokens=max_tokens
        )

        return response.choices[0].message.content

    # ---------------------------
    # 🔹 GEMINI
    # ---------------------------
    def _gemini_generate(self, prompt):
        response = self.client.generate_content(prompt)
        return response.text