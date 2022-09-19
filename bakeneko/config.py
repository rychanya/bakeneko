from pathlib import Path

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    TG_TOKEN: str = Field(..., env="TG_TOKEN")
    TG_WEB_APP_BASE: str = Field("tg-web-app")
    TG_WEB_HOOK_NAME: str = Field(..., env="TG_WEB_HOOK_NAME")
    BAKENEKO_HOST: str = Field(..., env="BAKENEKO_HOST")
    STORE_TYPE: str = Field("memory", env="STORE_TYPE")
    BASE_DIR: Path = Path.cwd()


# settings = Settings()  # type: ignore
