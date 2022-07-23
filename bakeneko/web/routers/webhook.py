from fastapi import APIRouter, Request

from bakeneko.bot import handle_update
from bakeneko.config import settings

router = APIRouter(prefix=f"/{settings.TG_WEB_HOOK_NAME}")


@router.post("/", include_in_schema=False)
async def webhook(request: Request):
    update = await request.json()
    await handle_update(update)
    return "ok"
