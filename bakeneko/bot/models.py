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


class Update(BaseModel):
    update_id: int
    message: Message | None
    inline_query: InlineQuery | None
