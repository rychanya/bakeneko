import hashlib
import hmac
from typing import cast

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from bakeneko.bot.models import User
from bakeneko.config import settings

router = APIRouter(prefix=f"/{settings.TG_WEB_APP_MENU}")

templates = Jinja2Templates(directory="/code/bakeneko/templates")


@router.get("/", response_class=HTMLResponse)
def root(request: Request):
    return templates.TemplateResponse(name="index.jinja", context={"request": request})


def check_init_data(request: Request) -> None:
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
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="init data invalid"
        )


class CheckInitData:
    _error = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail="init data invalid"
    )

    def __init__(
        self,
        auth_date: str | None = None,
        hash: str | None = None,
        query_id: str | None = None,
        user: str | None = None,
        can_send_after: str | None = None,
    ) -> None:
        if hash is None or auth_date is None or query_id is None or user is None:
            raise self._error
        init_data = cast(
            filter[str],
            filter(
                lambda v: v is not None, [auth_date, query_id, user, can_send_after]
            ),
        )
        data_check_string = "\n".join(sorted(init_data))
        secret_key = hmac.new(
            "WebAppData".encode(), settings.TG_TOKEN.encode(), hashlib.sha256
        ).digest()
        data_check = hmac.new(
            secret_key, data_check_string.encode(), hashlib.sha256
        ).hexdigest()
        if data_check != hash:
            raise self._error

        self.query_id = query_id
        self.user = User.parse_raw(user)


@router.post("/", )
async def root_post(init_data: CheckInitData = Depends()):
    # user = request.query_params.get("user")
    # print(type(user), user)
    print(init_data.query_id, init_data.user)
    return "ok"
