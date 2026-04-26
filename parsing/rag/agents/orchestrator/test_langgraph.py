from parsing.rag.agents.schemas.agent_schema import AgentState
from parsing.rag.agents.orchestrator.langgraph_flow import build_graph

graph = build_graph()

state = AgentState(
    query="improve this code",
    context="""
public int sum(int a, int b) {
    return a + b;
}
"""
)

result = graph.invoke(state)

print("\n=== FINAL OUTPUT ===\n")
print(result)