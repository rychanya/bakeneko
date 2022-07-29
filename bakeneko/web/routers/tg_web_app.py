from enum import Enum

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse

# from bakeneko.bot import bot
from bakeneko.config import settings
from bakeneko.templates import templates

# from telegram import (
#     InlineKeyboardButton,
#     InlineKeyboardMarkup,
#     InlineQueryResultArticle,
#     InputTextMessageContent,
# )

# from bakeneko.web.dependencies import CheckInitData

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


def get_menu_url():
    return router.url_path_for(RouterNames.MENU)


@router.post("/search/", name=RouterNames.SEARCH)
async def root_post(q: str = Form()):
    return q
