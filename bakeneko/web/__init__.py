from fastapi import FastAPI

from bakeneko.bot import bot
from bakeneko.config import settings
from bakeneko.db import engine, wait_until_db_ready
from bakeneko.db.scheme import Base
from bakeneko.web.routers import add_answer, question, webhook

app = FastAPI()
app.include_router(question.router)
app.include_router(add_answer.router)
app.include_router(webhook.router)


@app.on_event("startup")
async def start_up():
    wait_until_db_ready()
    Base.metadata.create_all(engine)
    if settings.BAKENEKO_HOST != "localhost":
        await bot.set_webhook(settings.web_hook_url)
