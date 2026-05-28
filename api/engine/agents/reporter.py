from langchain_core.messages import SystemMessage, HumanMessage
from llm.registry import get_llm
from engine.state import AgentState


REPORTER_PROMPT = """你是一个研究报告撰写专家。根据搜集到的信息，撰写一份结构清晰的研究报告。

要求：
- 使用中文撰写
- 包含引言、正文分析、结论
- 引用信息来源（标注URL）
- 语言专业但易懂
- 直接输出报告内容"""


def reporter(state: AgentState) -> dict:
    llm = get_llm(streaming=False)

    results_text = ""
    for r in state.search_results:
        results_text += f"- [{r.title}]({r.url}): {r.content}\n"

    analysis_text = ""
    for a in state.analysis:
        analysis_text += f"- 质量: {a.quality}, 评分: {a.score}/10, 总结: {a.summary}\n"

    response = llm.invoke([
        SystemMessage(content=REPORTER_PROMPT),
        HumanMessage(content=(
            f"研究问题：{state.question}\n\n"
            f"搜集到的信息：\n{results_text}\n\n"
            f"分析摘要：\n{analysis_text}"
        )),
    ])

    return {"report": response.content}
