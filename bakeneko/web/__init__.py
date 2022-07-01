from fastapi import FastAPI

from bakeneko.db.scheme import Base
from bakeneko.web.dependencies import engine_depend
from bakeneko.web.routers import question

app = FastAPI()
app.include_router(question.router)


@app.get("/")
async def root():
    return {"res": "ok"}


@app.on_event("startup")
def start_up():
    Base.metadata.create_all(engine_depend())
