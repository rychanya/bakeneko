from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from bakeneko.config import settings

router = APIRouter(prefix=f"/{settings.TG_WEB_APP_MENU}")

templates = Jinja2Templates(directory="/code/bakeneko/templates")


@router.get("/", response_class=HTMLResponse)
def root(request: Request):
    return templates.TemplateResponse(name="index.jinja", context={"request": request})

@router.post("/")
async def root_post(request: Request):
    json = await request.body()
    print(type(json), json)
    return "ok"
