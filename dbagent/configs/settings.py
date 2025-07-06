from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    db_backend: str | None = None
    db_host: str | None = None
    db_port: int | None = None
    db_user: str | None = None
    db_password: str | None = None
    db_name: str | None = None
    top_k: int | None = 19
    llm_model: str | None = None
    llm_provider: str | None = None
    openai_api_key: str | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )
    @property
    def database_url(self) -> str:
        host = self.db_host

        # If running locally (no docker), override host to localhost
        import os
        if os.environ.get("RUNNING_IN_DOCKER") != "true":
            host = "localhost"

        if not self.db_backend:
            raise ValueError("DB_BACKEND is not set")
            
        if self.db_backend.lower() == "postgresql":
            return f"postgresql://{self.db_user}:{self.db_password}@{host}:{self.db_port}/{self.db_name}"
        elif self.db_backend.lower() == "mysql":
            return f"mysql+pymysql://{self.db_user}:{self.db_password}@{host}:{self.db_port}/{self.db_name}"
        else:
            raise ValueError(f"Unsupported DB_BACKEND: {self.db_backend}")

settings = Settings()
