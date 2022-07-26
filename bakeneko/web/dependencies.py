import hashlib
import hmac

from fastapi import HTTPException, Request, status
from pydantic import ValidationError

from bakeneko.bot.models import User
from bakeneko.config import settings


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
