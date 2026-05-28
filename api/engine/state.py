from typing import Annotated, Literal
from operator import add

from langchain_core.messages import AnyMessage
from langgraph.graph import add_messages
from pydantic import BaseModel, Field


class SearchResult(BaseModel):
    url: str
    title: str
    content: str
    source: str


class AnalysisResult(BaseModel):
    sufficient: bool
    score: int = Field(ge=0, le=10)
    gaps: list[str]
    quality: Literal["low", "medium", "high"]
    summary: str


class AgentState(BaseModel):
    # 输入
    question: str = ""

    # 规划
    sub_questions: list[str] = []
    current_sub_index: int = 0

    # 检索
    search_results: Annotated[list[SearchResult], add] = []
    visited_urls: Annotated[list[str], add] = []

    # 分析
    analysis: Annotated[list[AnalysisResult], add] = []
    iteration: int = 0
    max_iterations: int = 3

    # 输出
    report: str = ""

    # LLM 对话历史
    messages: Annotated[list[AnyMessage], add_messages] = []
