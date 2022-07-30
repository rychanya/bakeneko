from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    POSTGRES_USER: str = Field(..., env="POSTGRES_USER")
    POSTGRES_PASSWORD: str = Field(..., env="POSTGRES_PASSWORD")
    POSTGRES_DB: str = Field(..., env="POSTGRES_DB")
    POSTGRES_PORT: str = Field(..., env="POSTGRES_PORT")
    TG_TOKEN: str = Field(..., env="TG_TOKEN")
    TG_WEB_APP_BASE: str = Field("tg-web-app")
    TG_WEB_HOOK_NAME: str = Field(..., env="TG_WEB_HOOK_NAME")
    BAKENEKO_HOST: str = Field(..., env="BAKENEKO_HOST")

    @property
    def db_url(self):
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@db:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    def get_abs_url(self, url):
        return f"https://{self.BAKENEKO_HOST}{url}"


settings = Settings()  # type: ignore
