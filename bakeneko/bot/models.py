from enum import Enum

from pydantic import BaseModel, Field


class WebAppData(BaseModel):
    data: str
    button_text: str


class User(BaseModel):
    id: int


class InlineQuery(BaseModel):
    id: str
    from_: User = Field(..., alias="from")
    query: str
    offset: str
    chat_type: str | None


class Message(BaseModel):
    message_id: int
    web_app_data: WebAppData | None


class CallbackQuery(BaseModel):
    id: str
    from_: User = Field(..., alias="from")
    data: str | None


class Update(BaseModel):
    update_id: int
    message: Message | None
    inline_query: InlineQuery | None
    callback_query: CallbackQuery | None


class CallBackAction(str, Enum):
    VOTE_UP = "VOTE_UP"
    VOTE_DOWN = "VOTE_DOWN"


class CallBackData(BaseModel):
    action: CallBackAction
    data: str
