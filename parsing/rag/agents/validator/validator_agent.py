import os
import logging

from parsing.rag.agents.schemas.agent_schema import AgentState, Validation
from parsing.rag.agents.utils.llm_client import LLMClient

logger = logging.getLogger(__name__)


class ValidatorAgent:

    def __init__(self):
        self.llm = LLMClient()
        self.prompt_template = self._load_prompt()

    # ---------------------------
    # 🔹 LOAD PROMPT
    # ---------------------------
    def _load_prompt(self):
        try:
            base_dir = os.path.dirname(os.path.dirname(__file__))
            prompt_path = os.path.join(base_dir, "prompts", "validator_prompt.txt")

            with open(prompt_path, "r", encoding="utf-8") as f:
                return f.read()

        except Exception:
            logger.exception("Failed to load validator prompt")
            raise RuntimeError("Prompt loading failed")

    # ---------------------------
    # 🔹 BUILD PROMPT
    # ---------------------------
    def _build_prompt(self, state: AgentState):
        code = state.refactor.code if state.refactor else state.context

        unit_tests = "\n".join(state.tests.unit_tests if state.tests else [])
        edge_cases = "\n".join(state.tests.edge_cases if state.tests else [])

        return self.prompt_template.format(
            code=code,
            unit_tests=unit_tests,
            edge_cases=edge_cases
        )

    # ---------------------------
    # 🔹 SAFE PARSE
    # ---------------------------
    def _safe_parse(self, text: str) -> Validation:
        import json

        try:
            data = json.loads(text)

            return Validation(
                is_valid=data.get("is_valid", False),
                confidence=float(data.get("confidence", 0.0)),
                errors=data.get("errors", []),
                warnings=data.get("warnings", [])   # 🔥 NEW
            )

        except Exception:
            logger.warning("Invalid JSON from validator")

            return Validation(
                is_valid=False,
                confidence=0.0,
                errors=["Failed to parse LLM response"],
                warnings=[]
            )

    # ---------------------------
    # 🚀 MAIN RUN
    # ---------------------------
    def run(self, state: AgentState) -> AgentState:
        try:
            logger.info("Running Validator Agent")

            prompt = self._build_prompt(state)

            response = self.llm.generate(prompt)

            validation = self._safe_parse(response)

            state.validation = validation

            return state

        except Exception:
            logger.exception("Validator agent failed")

            state.validation = Validation(
                is_valid=False,
                confidence=0.0,
                errors=["Validator failed"],
                warnings=[]   # 🔥 IMPORTANT
            )

            return state