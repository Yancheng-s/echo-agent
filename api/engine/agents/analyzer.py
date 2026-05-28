from engine.state import AgentState, AnalysisResult


def analyzer(state: AgentState) -> dict:
    # TODO: 填充分析 Agent
    return {
        "analysis": [AnalysisResult(
            sufficient=True, score=10, gaps=[], quality="high", summary=""
        )],
        "iteration": state.iteration + 1,
    }
