from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

SITE_DIR = Path.cwd().joinpath("web-vue", "dist")
SITE_BASE_URL = "/site"
SITE_NAME = "site"


def config_static_files(app: FastAPI):
    app.mount(SITE_BASE_URL, StaticFiles(directory=SITE_DIR), name=SITE_NAME)
