from dataclasses import dataclass
from enum import Enum


class QuestionType(str, Enum):
    ONE = "ONE"
    MANY = "MANY"
    ORDER = "ORDER"


IDType = str


@dataclass(frozen=True, slots=True, kw_only=True)
class Answer:
    answer_id: IDType
    question_id: IDType
    group_id: IDType | None
    answer: tuple[str, ...]
    is_correct: bool | None


@dataclass(frozen=True, slots=True, kw_only=True)
class AnswerDTO:
    question_id: IDType
    group_id: IDType | None
    answer: tuple[str, ...]
    is_correct: bool | None


@dataclass(frozen=True, slots=True, kw_only=True)
class Group:
    group_id: IDType
    question_id: IDType
    all_answers: frozenset[str]
    all_extra_answers: frozenset[str]


@dataclass(frozen=True, slots=True, kw_only=True)
class GroupDTO:
    question_id: IDType
    all_answers: frozenset[str]
    all_extra_answers: frozenset[str]


@dataclass(frozen=True, slots=True, kw_only=True)
class Question:
    text: str
    question_type: QuestionType
    question_id: IDType


@dataclass(frozen=True, slots=True, kw_only=True)
class QuestionDTO:
    text: str
    question_type: QuestionType
