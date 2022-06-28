from pydantic import UUID4, BaseModel

from bakeneko.models.types import AnswersList, ListOfNotEmptyStrings


class Answer(BaseModel):
    class Config:
        orm_mode = True

    question_id: UUID4
    is_correct: bool
    answer: AnswersList
    extra_answer: ListOfNotEmptyStrings = []


class AnswerInDB(Answer):
    answer_id: UUID4
