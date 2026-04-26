import logging
from parsing.rag.agents.schemas.agent_schema import AgentState

logger = logging.getLogger(__name__)


class StateManager:

    @staticmethod
    def init_state(state: AgentState) -> AgentState:
        """
        Ensure state is initialized properly
        """
        if not hasattr(state, "retry_count"):
            state.retry_count = 0

        return state

    # ---------------------------
    # 🔹 UPDATE METHODS
    # ---------------------------
    @staticmethod
    def update_analysis(state: AgentState, analysis):
        if not analysis:
            logger.warning("Empty analysis received")
            return state

        state.analysis = analysis
        return state

    @staticmethod
    def update_refactor(state: AgentState, refactor):
        if not refactor or not refactor.code:
            logger.warning("Invalid refactor output")
            return state

        state.refactor = refactor
        return state

    @staticmethod
    def update_tests(state: AgentState, tests):
        if not tests:
            logger.warning("Empty tests generated")
            return state

        state.tests = tests
        return state

    @staticmethod
    def update_validation(state: AgentState, validation):
        if not validation:
            logger.warning("Validation missing")
            return state

        state.validation = validation
        return state

    # ---------------------------
    # 🔹 RETRY HANDLING
    # ---------------------------
    @staticmethod
    def increment_retry(state: AgentState):
        state.retry_count = getattr(state, "retry_count", 0) + 1
        return state

    @staticmethod
    def reset_retry(state: AgentState):
        state.retry_count = 0
        return state