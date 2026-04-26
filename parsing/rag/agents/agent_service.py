import logging

from parsing.rag.agents.orchestrator.langgraph_flow import build_graph
from parsing.rag.agents.schemas.agent_schema import AgentState

logger = logging.getLogger(__name__)


class AgentService:

    def __init__(self):
        self.graph = build_graph()

    # ---------------------------
    # 🚀 RUN AGENT PIPELINE
    # ---------------------------
    def run(self, query: str, context: str) -> AgentState:
        try:
            logger.info("Starting Agent Pipeline")

            # 🔹 Initialize state
            state = AgentState(
                query=query,
                context=context
            )

            # 🔹 Run LangGraph
            final_state = self.graph.invoke(state)

            logger.info("Agent Pipeline Completed")

            return final_state

        except Exception:
            logger.exception("Agent pipeline failed")
            raise RuntimeError("Agent execution failed")