from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse

from bakeneko.web.static import SITE_NAME

router = APIRouter()


@router.get("/")
def redirect(request: Request):
    return RedirectResponse(request.url_for(SITE_NAME, path="/index.html"))
