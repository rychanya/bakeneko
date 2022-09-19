from dataclasses import dataclass
from uuid import UUID

from bakeneko.models.enums import TypeEnumDB


@dataclass
class AnswerDTO:
    question_id: UUID
    value: list[str]
    is_correct: bool


@dataclass
class AnswerDTOWithID(AnswerDTO):
    id_: UUID


@dataclass
class QuestionDTO:
    type_: TypeEnumDB
    text: str
    all_answers: list[str]
    all_extra_answers: list[str]
    answers: list[AnswerDTOWithID]


@dataclass
class QuestionDTOWithID(QuestionDTO):
    id_: UUID


@dataclass
class InsertDTO:
    type_: TypeEnumDB
    text: str
    all_answers: list[str]
    all_extra_answers: list[str]
    value: list[str]
    is_correct: bool


@dataclass
class InsertResultDTO:
    question: QuestionDTOWithID
    answer: AnswerDTOWithID
    is_new: bool


@dataclass
class SearchParams:
    q: str
    only_correct: bool = True
