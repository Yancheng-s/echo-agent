from langgraph.graph import StateGraph, END
from engine.state import AgentState
from engine.agents.planner import planner
from engine.agents.researcher import researcher
from engine.agents.analyzer import analyzer
from engine.agents.reporter import reporter


def route_after_analysis(state: AgentState) -> str:
    last = state.analysis[-1] if state.analysis else None
    if not last:
        return "researcher"
    if last.sufficient:
        return "reporter"
    if state.iteration >= state.max_iterations:
        return "reporter"
    return "researcher"


def build_graph():
    g = StateGraph(AgentState)
    g.add_node("planner", planner)
    g.add_node("researcher", researcher)
    g.add_node("analyzer", analyzer)
    g.add_node("reporter", reporter)

    g.set_entry_point("planner")
    g.add_edge("planner", "researcher")
    g.add_edge("researcher", "analyzer")
    g.add_conditional_edges("analyzer", route_after_analysis, {
        "researcher": "researcher",
        "reporter": "reporter",
    })
    g.add_edge("reporter", END)

    return g.compile()
