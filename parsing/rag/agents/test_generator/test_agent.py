import os
import logging

from parsing.rag.agents.schemas.agent_schema import AgentState, TestCases
from parsing.rag.agents.utils.llm_client import LLMClient

logger = logging.getLogger(__name__)


class TestAgent:

    def __init__(self):
        self.llm = LLMClient()
        self.prompt_template = self._load_prompt()

    # ---------------------------
    # 🔹 LOAD PROMPT
    # ---------------------------
    def _load_prompt(self):
        try:
            base_dir = os.path.dirname(os.path.dirname(__file__))
            prompt_path = os.path.join(base_dir, "prompts", "test_prompt.txt")

            with open(prompt_path, "r", encoding="utf-8") as f:
                return f.read()

        except Exception:
            logger.exception("Failed to load test prompt")
            raise RuntimeError("Prompt loading failed")

    # ---------------------------
    # 🔹 BUILD PROMPT
    # ---------------------------
    def _build_prompt(self, state: AgentState):
        code = ""

        if state.refactor and state.refactor.code:
            code = state.refactor.code
        else:
            code = state.context  # fallback

        return self.prompt_template.format(code=code)

    # ---------------------------
    # 🔹 SAFE PARSE
    # ---------------------------
    def _safe_parse(self, text: str) -> TestCases:
        import json

        try:
            data = json.loads(text)

            return TestCases(
                unit_tests=data.get("unit_tests", []),
                edge_cases=data.get("edge_cases", [])
            )

        except Exception:
            logger.warning("Invalid JSON from test agent")

            return TestCases(
                unit_tests=["Failed to parse LLM response"],
                edge_cases=[]
            )

    # ---------------------------
    # 🚀 MAIN RUN
    # ---------------------------
    def run(self, state: AgentState) -> AgentState:
        try:
            logger.info("Running Test Generator Agent")

            prompt = self._build_prompt(state)

            response = self.llm.generate(prompt)

            tests = self._safe_parse(response)

            state.tests = tests

            return state

        except Exception:
            logger.exception("Test agent failed")

            state.tests = TestCases(
                unit_tests=["Test generation failed"],
                edge_cases=[]
            )

            return state