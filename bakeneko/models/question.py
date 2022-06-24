from pydantic import UUID4, BaseModel, validator

from bakeneko.models.types import ListOfNotEmptyStrings, NotEmptyString, TypeEnum


class Question(BaseModel):
    class Config:
        orm_mode = True

    question_type: TypeEnum
    text: NotEmptyString
    all_answers: ListOfNotEmptyStrings = []
    all_extra_answers: ListOfNotEmptyStrings = []

    @validator("all_answers")
    def validate_all_answers(cls, all_answers: ListOfNotEmptyStrings | None):
        if all_answers and len(all_answers) < 2:
            raise ValueError("length of all answers must be more then two")
        return all_answers

    @validator("all_extra_answers")
    def validate_all_extra_answers(
        cls, all_extra_answers: ListOfNotEmptyStrings | None, values
    ):
        if all_extra_answers and len(all_extra_answers) < 2:
            raise ValueError("length of all extra answers must be more then two")
        question_type: TypeEnum | None = values.get("question_type")
        all_answers: ListOfNotEmptyStrings | None = values.get("all_answers")
        match question_type:
            case TypeEnum.ONE | TypeEnum.MANY | TypeEnum.ORDER:
                if all_extra_answers:
                    raise ValueError(
                        "all extra answers can be not empty only with MATCH type"
                    )
            case TypeEnum.MATCH:
                if all_extra_answers and not all_answers:
                    raise ValueError(
                        "all answers can not be empty if all extra answers presented"
                    )
                if (
                    all_extra_answers
                    and all_answers
                    and len(all_extra_answers) != len(all_answers)
                ):
                    raise ValueError(
                        "length of answers and extra answers must be same with no empty values"
                    )
        return all_extra_answers


class QuestionInDB(Question):
    question_id: UUID4
