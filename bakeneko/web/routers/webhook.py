from fastapi import APIRouter, Request

from bakeneko.bot import handle_update
from bakeneko.config import settings

router = APIRouter(prefix=f"/{settings.TG_TOKEN}")

WEB_HOOK_NAME = "tg-web-hook"


@router.post("/", include_in_schema=False, name=WEB_HOOK_NAME)
async def webhook(request: Request):
    update = await request.json()
    await handle_update(update)
    return "ok"


def get_webhook_url():
    return router.url_path_for(WEB_HOOK_NAME)
