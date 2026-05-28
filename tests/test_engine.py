"""
端到端测试：模拟用户输入，运行完整 research pipeline
用法：python tests/test_engine.py [问题]
"""
import sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / ".env")

sys.path.insert(0, str(Path(__file__).parent.parent / "api"))

from engine.graph import build_graph
from engine.state import AgentState


def run(question: str):
    print(f"问题: {question}")
    print("=" * 50)

    graph = build_graph()
    state = AgentState(question=question)
    result = graph.invoke(state)
    # LangGraph 返回 dict，统一转成 AgentState
    if isinstance(result, dict):
        result = AgentState(**result)

    print(f"\n子问题: {result.sub_questions}")
    print(f"搜索结果数: {len(result.search_results)}")
    print(f"迭代轮次: {result.iteration}")
    print(f"分析记录数: {len(result.analysis)}")
    print("=" * 50)
    print(f"\n{result.report}")


if __name__ == "__main__":
    question = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "2024年诺贝尔物理学奖颁给了谁？为什么？"
    run(question)
