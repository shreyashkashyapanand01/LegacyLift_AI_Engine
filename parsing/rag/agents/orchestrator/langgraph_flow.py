from langgraph.graph import StateGraph, END

from parsing.rag.agents.schemas.agent_schema import AgentState
from parsing.rag.agents.analyzer.analyzer_agent import AnalyzerAgent
from parsing.rag.agents.refactor.refactor_agent import RefactorAgent
from parsing.rag.agents.test_generator.test_agent import TestAgent
from parsing.rag.agents.validator.validator_agent import ValidatorAgent
from parsing.rag.agents.orchestrator.state_manager import StateManager

# 🔥 Router
from parsing.rag.agents.orchestrator.router import route_after_validation

# 🔥 NEW: Tracer
from parsing.rag.agents.utils.tracer import Tracer


# ---------------------------
# 🔹 AGENTS INIT
# ---------------------------
analyzer = AnalyzerAgent()
refactor = RefactorAgent()
tester = TestAgent()
validator = ValidatorAgent()


# ---------------------------
# 🔹 NODE FUNCTIONS (WITH TRACING 🔥)
# ---------------------------
def analyze_node(state: AgentState):
    state = StateManager.init_state(state)
    state = analyzer.run(state)
    state = StateManager.update_analysis(state, state.analysis)
    Tracer.log_step("analyze", state)
    return state


def refactor_node(state: AgentState):
    state = refactor.run(state)
    state = StateManager.update_refactor(state, state.refactor)
    Tracer.log_step("refactor", state)
    return state


def test_node(state: AgentState):
    state = tester.run(state)
    state = StateManager.update_tests(state, state.tests)
    Tracer.log_step("test", state)
    return state


def validate_node(state: AgentState):
    state = validator.run(state)
    state = StateManager.update_validation(state, state.validation)
    Tracer.log_step("validate", state)
    return state
# ---------------------------
# 🔹 BUILD GRAPH (ROUTER + TRACER 🔥)
# ---------------------------
def build_graph():

    builder = StateGraph(AgentState)

    # nodes
    builder.add_node("analyze", analyze_node)
    builder.add_node("refactor", refactor_node)
    builder.add_node("test", test_node)
    builder.add_node("validate", validate_node)

    # entry
    builder.set_entry_point("analyze")

    # flow
    builder.add_edge("analyze", "refactor")
    builder.add_edge("refactor", "test")
    builder.add_edge("test", "validate")

    # 🔥 CONDITIONAL ROUTING
    builder.add_conditional_edges(
        "validate",
        route_after_validation,
        {
            "refactor": "refactor",
            "end": END
        }
    )

    return builder.compile()