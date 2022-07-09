import asyncio

from fastapi import FastAPI

from bakeneko.bot import test_as
from bakeneko.db import engine, wait_until_db_ready
from bakeneko.db.scheme import Base
from bakeneko.web.routers import add_answer, question

app = FastAPI()
app.include_router(question.router)
app.include_router(add_answer.router)

tasks: set[asyncio.Task] = set()


@app.get("/")
async def root():
    return {"res": "ok"}


@app.on_event("startup")
async def start_up():
    wait_until_db_ready()
    Base.metadata.create_all(engine)
    tasks.add(asyncio.create_task(test_as()))


@app.on_event("shutdown")
async def shutdown():
    for task in tasks:
        task.cancel()
        await task
