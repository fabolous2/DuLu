from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    BOT_TOKEN: str
    DATABASE_URL: str
    BOT_URL: str
    YOUTUBE_API_KEY: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()

