"""
测试 LLM 连接：验证 API Key 是否有效，模型是否能正常响应
用法：python tests/test_llm.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "api"))

from llm.config import llm_settings
from llm.registry import get_llm

print(f"Provider: {llm_settings.llm_provider}")
print(f"Model:    {llm_settings.llm_model}")
print(f"Base URL: {llm_settings.llm_base_url}")
print("-" * 40)

llm = get_llm()
resp = llm.invoke("你好，请用一句话介绍你自己")
print(resp.content)
