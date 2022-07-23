import hashlib
import hmac

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
    json = request.query_params
    data_check_string = "\n".join(
        [
            f"{k}={request.query_params[k]}"
            for k in sorted(request.query_params.keys())
            if k != "hash"
        ]
    )
    secret_key = hmac.new("WebAppData".encode(), settings.TG_TOKEN.encode(), hashlib.sha256).digest()
    data_check = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()
    for k, v in json.items():
        print(f"{k} - {v}")
    print(data_check_string)
    print(secret_key)
    print(data_check)
    print(secret_key == json["hash"])
    return "ok"
