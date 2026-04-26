import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class Tracer:

    @staticmethod
    def log_step(step_name: str, state):
        logger.info(f"\n===== {step_name.upper()} =====")

        try:
            if hasattr(state, "analysis") and state.analysis:
                logger.info(f"Analysis: {state.analysis}")

            if hasattr(state, "refactor") and state.refactor:
                logger.info(f"Refactor: {state.refactor.code[:100]}...")

            if hasattr(state, "tests") and state.tests:
                logger.info(f"Tests count: {len(state.tests.unit_tests)}")

            if hasattr(state, "validation") and state.validation:
                logger.info(
                    f"Validation: valid={state.validation.is_valid}, "
                    f"confidence={state.validation.confidence}"
                )

            if hasattr(state, "retry_count"):
                logger.info(f"Retry count: {state.retry_count}")

        except Exception:
            logger.exception("Tracer failed")