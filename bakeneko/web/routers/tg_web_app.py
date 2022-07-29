from enum import Enum

from fastapi import APIRouter, Depends, Form, Request, Response
from fastapi.responses import HTMLResponse

from bakeneko.bot import select_answer_in_webapp
from bakeneko.config import settings
from bakeneko.templates import templates
from bakeneko.web.dependencies import CheckInitData

router = APIRouter(prefix=f"/{settings.TG_WEB_APP_BASE}")

emoji_dict = {True: "🟢", False: "🔴", None: "⚪"}


class RouterNames(str, Enum):
    MENU = "menu"
    SEARCH = "search"
    SELECT = "select"


@router.get("/menu/", response_class=HTMLResponse, name=RouterNames.MENU)
def menu(request: Request):
    return templates.TemplateResponse(
        name="tg/menu.jinja",
        context={
            "request": request,
        },
    )


@router.post("/search/", name=RouterNames.SEARCH)
async def search(request: Request, q: str = Form()):
    return templates.TemplateResponse(
        name="tg/answers.jinja",
        context={
            "request": request,
            "qas": [
                {
                    "id": "1",
                    "title": "title",
                    "type": "type",
                    "answers": ["1", "2", "3"],
                }
            ],
        },
    )


@router.post("/select/", name=RouterNames.SELECT)
async def select(
    response: Response, init_data: CheckInitData = Depends(), id: str = Form()
):
    await select_answer_in_webapp(init_data=init_data, answer_id=id)
    response.headers["HX-Trigger"] = "closeMenu"
    return "ok"
