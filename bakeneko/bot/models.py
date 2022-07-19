from pydantic import BaseModel


class WebAppData(BaseModel):
    data: str
    button_text: str


class Message(BaseModel):
    message_id: int
    web_app_data: WebAppData | None


class Update(BaseModel):
    update_id: int
    message: Message | None
