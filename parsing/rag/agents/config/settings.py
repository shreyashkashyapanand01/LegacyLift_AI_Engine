import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    # ---------------------------
    # 🔹 LLM CONFIG
    # ---------------------------
    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai").lower()
    LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", 0.2))

    # ---------------------------
    # 🔹 SYSTEM CONFIG
    # ---------------------------
    MAX_RETRIES = int(os.getenv("MAX_RETRIES", 2))

    # ---------------------------
    # 🔹 DEBUG
    # ---------------------------
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"