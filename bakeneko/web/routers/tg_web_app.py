import hashlib
import hmac

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError
from telegram import InlineQueryResultArticle, InputTextMessageContent

from bakeneko.bot import bot
from bakeneko.bot.models import User
from bakeneko.config import settings

router = APIRouter(prefix=f"/{settings.TG_WEB_APP_MENU}")

templates = Jinja2Templates(directory="/code/bakeneko/templates")


@router.get("/", response_class=HTMLResponse)
def root(request: Request):
    description = """
    🔴 Wrong
    🟢 Correct CorrectCorrectCorrectCorrectCorrectCorrectCorrectCorrect CorrectCorrectCorrectCorrect CorrectCorrectCorrectCorrect CorrectCorrectCorrectCorrect Correct
    ⚪ Long
    """
    return templates.TemplateResponse(name="index.jinja", context={"request": request, "description": description})


class CheckInitData:
    _error = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail="init data invalid"
    )

    def __init__(
        self,
        request: Request,
        hash: str,
    ) -> None:
        data_check_string = "\n".join(
            [
                f"{k}={request.query_params[k]}"
                for k in sorted(request.query_params.keys())
                if k
                in (
                    "query_id",
                    "user",
                    "receiver",
                    "chat",
                    "start_param",
                    "can_send_after",
                    "auth_date",
                )
            ]
        )
        secret_key = hmac.new(
            "WebAppData".encode(), settings.TG_TOKEN.encode(), hashlib.sha256
        ).digest()
        data_check = hmac.new(
            secret_key, data_check_string.encode(), hashlib.sha256
        ).hexdigest()
        if data_check != hash:
            raise self._error
        try:
            self.query_id = request.query_params["query_id"]
            self.user = User.parse_raw(request.query_params["user"])
        except (KeyError, ValidationError):
            raise self._error


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
