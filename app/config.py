from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite+aiosqlite:///must.db"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
