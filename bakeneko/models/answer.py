from pydantic import UUID4, BaseModel

from bakeneko.models.types import ListOfStrings, NotEmptyListOfStrings


class BaseAnswer(BaseModel):
    class Config:
        orm_mode = True

    is_correct: bool
    answer: NotEmptyListOfStrings
    extra_answer: ListOfStrings = []


class Answer(BaseAnswer):

    question_id: UUID4 | None = None


class AnswerInDB(Answer):
    answer_id: UUID4
