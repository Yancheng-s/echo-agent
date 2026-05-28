from engine.state import AgentState


def planner(state: AgentState) -> dict:
    # TODO: 填充规划 Agent
    return {"sub_questions": [state.question]}
