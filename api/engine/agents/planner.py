from pydantic import BaseModel, Field
from langchain_core.messages import SystemMessage, HumanMessage
from llm.registry import get_llm
from engine.state import AgentState


class PlanResult(BaseModel):
    sub_questions: list[str] = Field(description="拆解后的子问题列表，按优先级排列")


PLANNER_PROMPT = """你是一个研究规划专家。给定一个研究问题，将其拆解为2-5个可独立搜索的子问题。

要求：
- 每个子问题具体、可搜索
- 子问题之间互补，覆盖原始问题的不同方面
- 按优先级排列"""


def planner(state: AgentState) -> dict:
    llm = get_llm(streaming=False)
    structured_llm = llm.with_structured_output(PlanResult, method="function_calling")
    result = structured_llm.invoke([
        SystemMessage(content=PLANNER_PROMPT),
        HumanMessage(content=f"研究问题：{state.question}"),
    ])
    return {"sub_questions": result.sub_questions}
