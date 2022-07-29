from enum import Enum

from fastapi import APIRouter, Depends, Form, Request, Response
from fastapi.responses import HTMLResponse

from bakeneko import store
from bakeneko.bot import select_answer_in_webapp
from bakeneko.config import settings
from bakeneko.templates import templates
from bakeneko.web.dependencies import CheckInitData

router = APIRouter(prefix=f"/{settings.TG_WEB_APP_BASE}")


class RouterNames(str, Enum):
    MENU = "menu"
    SEARCH = "search"
    SELECT = "select"
    ANSWER = "answer"


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
        context={"request": request, "qas": await store.search(q)},
    )


@router.post("/select/", name=RouterNames.SELECT)
async def select(
    response: Response, init_data: CheckInitData = Depends(), id: str = Form()
):
    answer_url = settings.get_abs_url(
        router.url_path_for(RouterNames.ANSWER, answer_id=id)
    )
    await select_answer_in_webapp(
        init_data=init_data, answer_id=id, answer_url=answer_url
    )
    response.headers["HX-Trigger"] = "closeMenu"
    return "ok"


@router.get("/answer/{answer_id}/", name=RouterNames.ANSWER)
async def get_answer(request: Request, answer_id: str):
    qa = await store.get_answer_by_id(answer_id)
    return templates.TemplateResponse(
        name="tg/answer.jinja",
        context={
            "request": request,
            "qa": qa,
            "og_title": qa["title"],
            "og_description": "\n".join(qa["answers"]),
        },
    )
