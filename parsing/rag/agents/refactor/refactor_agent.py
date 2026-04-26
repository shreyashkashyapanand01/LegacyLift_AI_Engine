import os
import logging

from parsing.rag.agents.schemas.agent_schema import AgentState, Refactor
from parsing.rag.agents.utils.llm_client import LLMClient

logger = logging.getLogger(__name__)


class RefactorAgent:

    def __init__(self):
        self.llm = LLMClient()
        self.prompt_template = self._load_prompt()

    # ---------------------------
    # 🔹 LOAD PROMPT
    # ---------------------------
    def _load_prompt(self):
        try:
            base_dir = os.path.dirname(os.path.dirname(__file__))
            prompt_path = os.path.join(base_dir, "prompts", "refactor_prompt.txt")

            with open(prompt_path, "r", encoding="utf-8") as f:
                return f.read()

        except Exception:
            logger.exception("Failed to load refactor prompt")
            raise RuntimeError("Prompt loading failed")

    # ---------------------------
    # 🔹 BUILD PROMPT
    # ---------------------------
    def _build_prompt(self, state: AgentState):
        return self.prompt_template.format(
            context=state.context,
            issues=", ".join(state.analysis.issues if state.analysis else []),
            suggestions=", ".join(state.analysis.suggestions if state.analysis else [])
        )

    # ---------------------------
    # 🔹 JSON CLEANER (NEW)
    # ---------------------------
    def _clean_json(self, text: str) -> str:
        import re

        # remove markdown
        text = re.sub(r"```json|```", "", text)

        # trim
        text = text.strip()

        # extract JSON block
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            return match.group(0)

        return text

    # ---------------------------
    # 🔹 SAFE PARSE (FIXED)
    # ---------------------------
    def _safe_parse(self, text: str) -> Refactor:
        import json

        # 🔹 First attempt
        try:
            cleaned = self._clean_json(text)
            data = json.loads(cleaned)

            return Refactor(
                code=data.get("code", ""),
                changes=data.get("changes", []),
                explanation=data.get("explanation", "")
            )

        except Exception:
            logger.warning("Invalid JSON from refactor agent (retrying once)")

            # 🔁 Retry once with strict instruction
            try:
                retry_prompt = (
                    "Fix this into VALID JSON ONLY.\n"
                    "Return ONLY JSON. No explanation.\n\n"
                    + text
                )

                retry_response = self.llm.generate(retry_prompt)

                cleaned = self._clean_json(retry_response)
                data = json.loads(cleaned)

                return Refactor(
                    code=data.get("code", ""),
                    changes=data.get("changes", []),
                    explanation=data.get("explanation", "")
                )

            except Exception:
                logger.error("Refactor agent failed after retry")

                return Refactor(
                    code="",
                    changes=["Failed to parse LLM response"],
                    explanation=""
                )

    # ---------------------------
    # 🚀 MAIN RUN
    # ---------------------------
    def run(self, state: AgentState) -> AgentState:
        try:
            logger.info("Running Refactor Agent")

            prompt = self._build_prompt(state)

            response = self.llm.generate(prompt)

            refactor = self._safe_parse(response)

            state.refactor = refactor

            return state

        except Exception:
            logger.exception("Refactor agent failed")

            state.refactor = Refactor(
                code="",
                changes=["Refactor failed"],
                explanation=""
            )

            return state