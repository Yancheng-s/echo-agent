from langchain_openai import ChatOpenAI
from core.config import llm_settings

# 模型注册表：名字 → (base_url, 默认模型)
PROVIDERS = {
    "zhipu": ("https://open.bigmodel.cn/api/paas/v4", "glm-4"),
    "deepseek": ("https://api.deepseek.com", "deepseek-chat"),
    "moonshot": ("https://api.moonshot.cn/v1", "moonshot-v1-8k"),
    "qwen": ("https://dashscope.aliyuncs.com/compatible-mode/v1", "qwen-plus"),
    "openai": ("https://api.openai.com/v1", "gpt-4o"),
}


def get_llm(
    provider: str = None,
    model: str = None,
    temperature: float = None,
    max_tokens: int = None,
    streaming: bool = True,
) -> ChatOpenAI:
    provider = provider or llm_settings.llm_provider
    base_url, default_model = PROVIDERS.get(provider, (llm_settings.llm_base_url, llm_settings.llm_model))

    return ChatOpenAI(
        model=model or llm_settings.llm_model or default_model,
        api_key=llm_settings.llm_api_key,
        base_url=base_url,
        temperature=temperature or llm_settings.llm_temperature,
        max_tokens=max_tokens or llm_settings.llm_max_tokens,
        streaming=streaming,
    )
