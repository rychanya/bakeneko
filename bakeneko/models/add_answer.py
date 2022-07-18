from pydantic import BaseModel, validator

from bakeneko.models.answer import AnswerInDB, BaseAnswer
from bakeneko.models.question import Question, QuestionInDB
from bakeneko.models.types import TypeEnum


class AddAnswer(Question):
    answer: BaseAnswer

    @validator("answer")
    def validate_answers(cls, v: BaseAnswer, values):
        match values:
            case {"question_type": TypeEnum.ONE, "all_answers": _all_answers}:
                if _all_answers and not set(v.answer).issubset(_all_answers):
                    raise ValueError(
                        "answers must be subset of all answers from question"
                    )
                if len(v.answer) != 1:
                    raise ValueError("answer with type ONE can contain only one item")
                if v.extra_answer:
                    raise ValueError("answer with type ONE can not have extra answers")
            case {"question_type": TypeEnum.MANY, "all_answers": _all_answers}:
                if _all_answers and not set(v.answer).issubset(_all_answers):
                    raise ValueError(
                        "answer must be subset of all answers from question"
                    )
                if v.extra_answer:
                    raise ValueError("answer with type MANY can not have extra answers")
            case {"question_type": TypeEnum.ORDER, "all_answers": _all_answers}:
                if _all_answers and set(v.answer) != set(_all_answers):
                    raise ValueError(
                        "answer with type ORDER must contain all answers from question"
                    )
                if v.extra_answer:
                    raise ValueError(
                        "answer with type ORDER can not have extra answers"
                    )
            case {
                "question_type": TypeEnum.MATCH,
                "all_answers": _all_answers,
                "all_extra_answers": _all_extra_answers,
            }:
                if _all_answers and set(v.answer) != set(_all_answers):
                    raise ValueError(
                        "answer with type MATCH must contain all answers from question"
                    )
                if (
                    _all_extra_answers
                    and v.extra_answer
                    and set(v.extra_answer) != set(_all_extra_answers)
                ):
                    raise ValueError(
                        "answer with type MATCH must contain all extra answers from question"
                    )
                if v.extra_answer and len(v.extra_answer) != len(v.answer):
                    raise ValueError("extra answer must have same length as answer")
        return v


class AddAnswerResponse(BaseModel):
    is_new_question: bool
    question: QuestionInDB
    is_new_answer: bool
    answer: AnswerInDB
