from fastapi import FastAPI

from bakeneko.web.routes import answer, home


def config_routes(app: FastAPI):
    app.include_router(answer.router)
    app.include_router(home.router)
