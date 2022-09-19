import hashlib
import hmac
from urllib.parse import parse_qsl

from fastapi import Form, HTTPException, status
from pydantic import ValidationError

from bakeneko.config import settings


class CheckInitData:
    _error = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail="init data invalid"
    )

    def __init__(
        self,
        init: str = Form(),
    ) -> None:
        init_dict = dict(parse_qsl(init))
        hash = init_dict.pop("hash", "")
        data_check_string = "\n".join(
            [f"{k}={init_dict[k]}" for k in sorted(init_dict.keys())]
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
            self.query_id = init_dict["query_id"]
            # self.user = User.parse_raw(init_dict["user"])
        except (KeyError, ValidationError):
            raise self._error
