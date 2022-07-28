from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InlineQueryResultArticle,
    InputTextMessageContent,
)

from bakeneko.bot import bot
from bakeneko.config import settings
from bakeneko.templates import templates
from bakeneko.web.dependencies import CheckInitData

router = APIRouter(prefix=f"/{settings.TG_WEB_APP_MENU}")


@router.get("/", response_class=HTMLResponse)
def root(request: Request, fname: str = Query("")):
    print(fname)
    og_title = "og title"
    description = "\n".join(
        [
            "🔴 Wrong",
            "🟢 Correct",
            "⚪ Long",
        ]
    )
    qas = [
        {
            "title": "what?",
            "type": "only one",
            "answers": [
                {"text": "correct", "is_correct": True},
                {"text": "incorrect", "is_correct": False},
                {"text": "normal", "is_correct": None},
            ],
        },
        {
            "title": "what?",
            "type": "only one",
            "answers": [
                {"text": "correct", "is_correct": True},
                {"text": "incorrect", "is_correct": False},
                {"text": "normal", "is_correct": None},
            ],
        },
        {
            "title": "what?",
            "type": "only one",
            "answers": [
                {"text": "correct", "is_correct": True},
                {"text": "incorrect", "is_correct": False},
                {"text": "normal", "is_correct": None},
            ],
        },
    ]
    return templates.TemplateResponse(
        name="index.jinja",
        context={
            "request": request,
            "og_description": description,
            "og_title": og_title,
            "qas": qas,
            "fname": fname,
        },
    )

class QAID(BaseModel):
    id: str

@router.post(
    "/",
)
async def root_post(qaid: QAID, init_data: CheckInitData = Depends()):
    await bot.answer_web_app_query(
        web_app_query_id=init_data.query_id,
        result=InlineQueryResultArticle(
            id="1",
            title="title",
            description="des",
            input_message_content=InputTextMessageContent(
                message_text=qaid.id, parse_mode=None, disable_web_page_preview=False
            ),
            reply_markup=InlineKeyboardMarkup.from_button(InlineKeyboardButton(text="Share", switch_inline_query=qaid.id))
        ),
    )

    return "ok"


@router.get("/json/")
def json():
    return JSONResponse(
        [
            {"id": "1", "title": "test", "type": "type", "answers": ["jujjj", "jjjj"]},
            {"id": "2", "title": "test", "type": "type", "answers": ["jujjj", "jjjj"]},
        ]
    )
