from typing import Mapping

from pydantic import BaseModel, validator

from bakeneko.models.types import (
    ListOfStrings,
    NotEmptyListOfStrings,
    NotEmptyString,
    TypeEnum,
)


class DBMixin(BaseModel):
    id: str
    by: str


class Answer(BaseModel):
    question: NotEmptyString
    type: TypeEnum
    all_answers: ListOfStrings = []
    all_extra_answers: ListOfStrings = []
    answer: NotEmptyListOfStrings
    extra_answer: ListOfStrings = []
    is_correct: bool

    @validator("all_answers")
    def check_all_answers(cls, v: ListOfStrings | None):
        if v:
            if len(v) < 2:
                raise ValueError
            return sorted(v)
        return v

    @validator("all_extra_answers")
    def check_all_extra_answers(cls, v: ListOfStrings | None, values: Mapping):
        if v:
            type: TypeEnum | None = values.get("type")
            if type and type != TypeEnum.MATCH:
                raise ValueError
            if len(v) < 2:
                raise ValueError
            return sorted(v)
        return v

    @validator("answer")
    def check_answer(cls, v: NotEmptyListOfStrings | None, values: Mapping):
        if v:
            type: TypeEnum | None = values.get("type")
            all_answers: list[str] | None = values.get("all_answers")
            match type:
                case TypeEnum.ONE:
                    if len(v) != 1:
                        raise ValueError
                    if all_answers and not set(v).issubset(all_answers):
                        raise ValueError
                    return v
                case TypeEnum.MANY:
                    if all_answers and not set(v).issubset(all_answers):
                        raise ValueError
                    return sorted(v)
                case TypeEnum.ORDER | TypeEnum.MATCH:
                    if all_answers and set(v) != set(all_answers):
                        raise ValueError
                    return v
        return v

    @validator("extra_answer")
    def check_extra_answer(cls, v: ListOfStrings | None, values: Mapping):
        if v:
            type: TypeEnum | None = values.get("type")
            if type and type != TypeEnum.MATCH:
                raise ValueError
            all_extra_answers: list[str] | None = values.get("all_extra_answers")
            if all_extra_answers and set(v) != set(all_extra_answers):
                raise ValueError
            answer: ListOfStrings | None = values.get("answer")
            if answer is None:
                raise ValueError
            elif len(v) != len(answer):
                raise ValueError
        return v


class AnswerDB(Answer, DBMixin):
    ...
