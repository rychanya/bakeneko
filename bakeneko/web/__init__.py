from pprint import pprint

from fastapi import FastAPI, Request

from bakeneko.db import engine, wait_until_db_ready
from bakeneko.db.scheme import Base
from bakeneko.web.routers import add_answer, question

app = FastAPI()
app.include_router(question.router)
app.include_router(add_answer.router)


@app.get("/")
async def root():
    return {"res": "ok"}


@app.post("/secretwebhook")
async def webhook(request: Request):
    update = await request.json()
    pprint(update)
    return "ok"


@app.on_event("startup")
async def start_up():
    wait_until_db_ready()
    Base.metadata.create_all(engine)
