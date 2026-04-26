import logging
from parsing.rag.agents.schemas.agent_schema import AgentState
from parsing.rag.agents.orchestrator.state_manager import StateManager
from parsing.rag.agents.config.settings import Settings

logger = logging.getLogger(__name__)


MAX_RETRIES = Settings.MAX_RETRIES


def route_after_validation(state: AgentState) -> str:
    """
    Decide next step after validation
    """

    if not state.validation:
        logger.warning("No validation found, ending flow")
        return "end"

    # 🔥 SUCCESS CASE
    if state.validation.is_valid:
        logger.info("Validation passed -> ending flow")
        return "end"

    # 🔥 FAILURE CASE → retry
    retries = getattr(state, "retry_count", 0)

    if retries < MAX_RETRIES:
        logger.warning(f"Validation failed -> retrying refactor ({retries + 1})")

        # increment retry count
        state = StateManager.increment_retry(state)

        return "refactor"

    # 🔥 MAX RETRIES HIT
    logger.error("Max retries reached -> ending flow")

    return "end"