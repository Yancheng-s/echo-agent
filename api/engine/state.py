from typing import Annotated
from operator import add
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
    quality: str  # low / medium / high
    summary: str


class AgentState(BaseModel):
    question: str = ""
    sub_questions: list[str] = []
    current_sub_index: int = 0
    search_results: Annotated[list[SearchResult], add] = []
    analysis: Annotated[list[AnalysisResult], add] = []
    report: str = ""
    iteration: int = 0
    max_iterations: int = 3
