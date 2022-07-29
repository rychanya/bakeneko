from enum import Enum

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse

# from bakeneko.bot import bot
from bakeneko.config import settings
from bakeneko.templates import templates
from bakeneko.web.dependencies import CheckInitData

# from telegram import (
#     InlineKeyboardButton,
#     InlineKeyboardMarkup,
#     InlineQueryResultArticle,
#     InputTextMessageContent,
# )


router = APIRouter(prefix=f"/{settings.TG_WEB_APP_BASE}")

emoji_dict = {True: "🟢", False: "🔴", None: "⚪"}


class RouterNames(str, Enum):
    MENU = "menu"
    SEARCH = "search"


@router.get("/menu/", response_class=HTMLResponse, name=RouterNames.MENU)
def root(request: Request):
    return templates.TemplateResponse(
        name="tg/menu.jinja",
        context={
            "request": request,
        },
    )


@router.post("/search/", name=RouterNames.SEARCH)
async def root_post(q: str = Form(), init: str = Form()):
    return f"{q}  {init}"
