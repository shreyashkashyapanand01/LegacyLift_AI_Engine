from parsing.rag.agents.analyzer.analyzer_agent import AnalyzerAgent
from parsing.rag.agents.refactor.refactor_agent import RefactorAgent
from parsing.rag.agents.test_generator.test_agent import TestAgent
from parsing.rag.agents.schemas.agent_schema import AgentState

state = AgentState(
    query="generate tests",
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

# Step 3: Generate Tests
state = TestAgent().run(state)

print("\n=== TESTS ===\n")
print(state.tests)