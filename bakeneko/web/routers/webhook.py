from fastapi import APIRouter, Request

from bakeneko.bot import handle_update

router = APIRouter(prefix="/secretwebhook", tags=["webhook"])


@router.post("/")
async def webhook(request: Request):
    update = await request.json()
    await handle_update(update)
    return "ok"
