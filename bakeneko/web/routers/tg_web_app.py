import hashlib
import hmac

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from bakeneko.config import settings

router = APIRouter(prefix=f"/{settings.TG_WEB_APP_MENU}")

templates = Jinja2Templates(directory="/code/bakeneko/templates")


@router.get("/", response_class=HTMLResponse)
def root(request: Request):
    return templates.TemplateResponse(name="index.jinja", context={"request": request})

def check_init_data(request: Request)->None:
    data_check_string = "\n".join(
        [
            f"{k}={request.query_params[k]}"
            for k in sorted(request.query_params.keys())
            if k != "hash"
        ]
    )
    secret_key = hmac.new(
        "WebAppData".encode(), settings.TG_TOKEN.encode(), hashlib.sha256
    ).digest()
    data_check = hmac.new(
        secret_key, data_check_string.encode(), hashlib.sha256
    ).hexdigest()
    if data_check != request.query_params.get("hash"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="init data invalid")


@router.post("/", dependencies=[Depends(check_init_data)])
async def root_post(request: Request):
    user = request.query_params.get("user")
    print(type(user), user)
    return "ok"
