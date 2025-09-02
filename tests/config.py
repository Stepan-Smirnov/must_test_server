from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    TEST_DATABASE_URL: str = "sqlite+aiosqlite:///test_must.db"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
