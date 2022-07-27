from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from telegram import InlineQueryResultArticle, InputTextMessageContent

from bakeneko.bot import bot
from bakeneko.config import settings
from bakeneko.templates import templates
from bakeneko.web.dependencies import CheckInitData

router = APIRouter(prefix=f"/{settings.TG_WEB_APP_MENU}")


@router.get("/", response_class=HTMLResponse)
def root(request: Request):
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
        },
    )


@router.post(
    "/",
)
async def root_post(init_data: CheckInitData = Depends()):
    await bot.answer_web_app_query(
        web_app_query_id=init_data.query_id,
        result=InlineQueryResultArticle(
            id="1",
            title="title",
            description="des",
            input_message_content=InputTextMessageContent(
                message_text="text", parse_mode=None, disable_web_page_preview=False
            ),
        ),
    )

    return "ok"
