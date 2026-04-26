from parsing.rag.agents.analyzer.analyzer_agent import AnalyzerAgent
from parsing.rag.agents.refactor.refactor_agent import RefactorAgent
from parsing.rag.agents.test_generator.test_agent import TestAgent
from parsing.rag.agents.validator.validator_agent import ValidatorAgent
from parsing.rag.agents.schemas.agent_schema import AgentState

state = AgentState(
    query="improve this code",
    context="""
public int sum(int a, int b) {
    return a + b;
}
"""
)

# Pipeline
state = AnalyzerAgent().run(state)
state = RefactorAgent().run(state)
state = TestAgent().run(state)
state = ValidatorAgent().run(state)

print("\n=== FINAL STATE ===\n")
print(state.validation)