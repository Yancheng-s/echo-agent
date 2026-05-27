from pydantic_settings import BaseSettings


class LLMSettings(BaseSettings):
    llm_provider: str = "zhipu"
    llm_model: str = "glm-4"
    llm_api_key: str = "your-api-key"
    llm_base_url: str = "https://open.bigmodel.cn/api/paas/v4"
    llm_temperature: float = 0.7
    llm_max_tokens: int = 4096

    model_config = {"env_file": ".env", "extra": "ignore"}


llm_settings = LLMSettings()
