from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    DATABASE_URL: str

    SUPABASE_URL: str
    SUPABASE_KEY: str
    OLLAMA_URL: str = "http://127.0.0.1:11434"
    OLLAMA_MODEL: str = "qwen3:8b"
    OLLAMA_TIMEOUT_SECS: int = 120
    OLLAMA_NUM_CTX: int = 2048
    OLLAMA_NUM_PREDICT: int = 220
    OLLAMA_TEMPERATURE: float = 0.0

    model_config = SettingsConfigDict(
        env_file=".env"
    )

    @property
    def async_database_url(self) -> str:

        if self.DATABASE_URL.startswith("postgresql://"):
            return self.DATABASE_URL.replace(
                "postgresql://",
                "postgresql+asyncpg://",
                1
            )

        return self.DATABASE_URL


settings = Settings()