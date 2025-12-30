from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "AI Print Estimator"
    ENV: str = "dev"

    DATABASE_URL: str = "postgresql://admin:admin@db:5432/printdb"

    OPENAI_API_KEY: str

    N8N_WEBHOOK_URL: str = "http://n8n:5678/webhook/print-estimator"

    class Config:
        env_file = ".env"


settings = Settings()