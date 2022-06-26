from pydantic import UUID4, BaseModel

from bakeneko.models.types import AnswersList


class Answer(BaseModel):
    class Config:
        orm_mode = True

    question_id: UUID4
    is_correct: bool
    answer: AnswersList


class AnswerInDB(Answer):
    answer_id: UUID4
