from langchain_core.messages import SystemMessage, HumanMessage
from llm.registry import get_llm
from engine.state import AgentState, AnalysisResult


ANALYZER_PROMPT = """你是一个研究质量评估专家。评估已搜集的信息是否足够回答原始研究问题。

评估标准：
- 信息是否覆盖了问题的各个方面
- 信息来源是否可靠
- 是否有明显的知识缺口

返回评估结果，包括：
- sufficient: 信息是否足够回答问题
- score: 质量评分 0-10
- gaps: 还缺少什么（如充分则为空列表）
- quality: low / medium / high
- summary: 当前信息的简要总结"""


def analyzer(state: AgentState) -> dict:
    llm = get_llm(streaming=False)
    structured_llm = llm.with_structured_output(AnalysisResult, method="function_calling")

    results_text = ""
    for r in state.search_results:
        results_text += f"- [{r.title}]({r.url}): {r.content}\n"

    gaps_hint = ""
    if state.analysis:
        last = state.analysis[-1]
        if last.gaps:
            gaps_hint = f"\n上一轮指出缺少：{', '.join(last.gaps)}"

    result = structured_llm.invoke([
        SystemMessage(content=ANALYZER_PROMPT),
        HumanMessage(content=(
            f"原始问题：{state.question}\n\n"
            f"已搜集信息：\n{results_text}\n"
            f"第 {state.iteration + 1} 轮评估{gaps_hint}"
        )),
    ])

    return {
        "analysis": [result],
        "iteration": state.iteration + 1,
    }
