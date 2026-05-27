from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql+psycopg://postgres:root@localhost:5432/echo_agent"
    jwt_secret: str = "change-this-to-a-random-secret"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60 * 24  # 24 小时

    model_config = {"env_file": ".env"}


settings = Settings()
