from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from bakeneko.bot import init_bot
from bakeneko.config import settings
from bakeneko.db import engine, wait_until_db_ready
from bakeneko.db.scheme import Base
from bakeneko.web.routers import add_answer, question, tg_web_app, webhook

app = FastAPI()
app.mount("/static", StaticFiles(directory="/code/bakeneko/static"), name="static")
app.include_router(question.router)
app.include_router(add_answer.router)
app.include_router(webhook.router)
app.include_router(tg_web_app.router)


@app.on_event("startup")
async def start_up():
    wait_until_db_ready()
    Base.metadata.create_all(engine)
    print(10 * "*")
    print(webhook.get_webhook_url())
    if settings.BAKENEKO_HOST != "localhost":
        await init_bot(
            web_hook_url=settings.get_abs_url(webhook.get_webhook_url()),
            web_app_menu_url=settings.get_abs_url(tg_web_app.get_menu_url()),
        )
