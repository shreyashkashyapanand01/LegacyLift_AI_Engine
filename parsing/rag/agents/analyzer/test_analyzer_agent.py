from parsing.rag.agents.analyzer.analyzer_agent import AnalyzerAgent
from parsing.rag.agents.schemas.agent_schema import AgentState

state = AgentState(
    query="analyze this code",
    context="""
File: A.java
Function: sum

public int sum(int a, int b) {
    return a + b;
}
"""
)

agent = AnalyzerAgent()
new_state = agent.run(state)

print(new_state.analysis)