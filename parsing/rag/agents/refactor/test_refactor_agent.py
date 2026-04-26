from parsing.rag.agents.analyzer.analyzer_agent import AnalyzerAgent
from parsing.rag.agents.refactor.refactor_agent import RefactorAgent
from parsing.rag.agents.schemas.agent_schema import AgentState

state = AgentState(
    query="refactor this code",
    context="""
public int sum(int a, int b) {
    return a + b;
}
"""
)

# Step 1: Analyze
state = AnalyzerAgent().run(state)

# Step 2: Refactor
state = RefactorAgent().run(state)

print("\n=== REFACTORED ===\n")
print(state.refactor)