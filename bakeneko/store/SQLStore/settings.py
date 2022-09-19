from pydantic import BaseSettings

from bakeneko.settings import ENV_FILE_PATH


class QAStoreSettings(BaseSettings):
    class Config:
        env_prefix = "bakeneko_db_"

    dialect: str = "postgresql"
    driver: str = "asyncpg"
    username: str
    password: str
    host: str = "localhost"
    port: int = 5432
    database: str = "db"
    echo: bool = False

    @property
    def db_url(self):
        return f"{self.dialect}+{self.driver}://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"


settings = QAStoreSettings(_env_file=ENV_FILE_PATH)  # type: ignore
