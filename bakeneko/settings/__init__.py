from pathlib import Path

from pydantic import BaseSettings

from bakeneko.models.enums import StoreType

ENV_FILE_PATH = Path(".env")


class AppSettings(BaseSettings):
    store_type: StoreType = StoreType.SQLStore


app_settings = AppSettings()
