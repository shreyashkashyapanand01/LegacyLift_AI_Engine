import os
import logging
from typing import Optional

from parsing.rag.agents.schemas.agent_schema import AgentState, Analysis
from parsing.rag.agents.utils.llm_client import LLMClient

logger = logging.getLogger(__name__)


class AnalyzerAgent:

    def __init__(self):
        self.llm = LLMClient()
        self.prompt_template = self._load_prompt()

    # ---------------------------
    # 🔹 LOAD PROMPT
    # ---------------------------
    def _load_prompt(self) -> str:
        try:
            base_dir = os.path.dirname(os.path.dirname(__file__))
            prompt_path = os.path.join(base_dir, "prompts", "analyzer_prompt.txt")

            with open(prompt_path, "r", encoding="utf-8") as f:
                return f.read()

        except Exception:
            logger.exception("Failed to load analyzer prompt")
            raise RuntimeError("Prompt loading failed")

    # ---------------------------
    # 🔹 BUILD PROMPT
    # ---------------------------
    def _build_prompt(self, state: AgentState) -> str:
        return self.prompt_template.format(
            context=state.context,
            query=state.query
        )

    # ---------------------------
    # 🔹 SAFE JSON PARSE
    # ---------------------------
    def _safe_parse(self, text: str) -> Analysis:
        import json

        try:
            data = json.loads(text)

            return Analysis(
                issues=data.get("issues", []),
                patterns=data.get("patterns", []),
                suggestions=data.get("suggestions", [])
            )

        except Exception:
            logger.warning("LLM returned invalid JSON, using fallback")

            return Analysis(
                issues=["Failed to parse LLM response"],
                patterns=[],
                suggestions=[]
            )

    # ---------------------------
    # 🚀 MAIN EXECUTION
    # ---------------------------
    def run(self, state: AgentState) -> AgentState:
        try:
            logger.info("Running Analyzer Agent")

            prompt = self._build_prompt(state)

            response = self.llm.generate(prompt)

            analysis = self._safe_parse(response)

            # 🔥 Update state
            state.analysis = analysis

            return state

        except Exception:
            logger.exception("Analyzer agent failed")

            # fallback state (never break pipeline)
            state.analysis = Analysis(
                issues=["Analyzer failed"],
                patterns=[],
                suggestions=[]
            )

            return state