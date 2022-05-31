from dataclasses import dataclass

from bakeneko.store.base import Store
from bakeneko.store.types import (
    Answer,
    AnswerDTO,
    Group,
    GroupDTO,
    Question,
    QuestionDTO,
    QuestionType,
)


@dataclass(frozen=True, slots=True, kw_only=True)
class AddAnswerDTO:
    text: str
    question_type: QuestionType
    all_answers: frozenset[str]
    all_extra_answers: frozenset[str]
    answer: tuple[str, ...]
    is_correct: bool | None


@dataclass(frozen=True, slots=True, kw_only=True)
class AddAnswerResultDTO:
    question: Question
    group: Group | None
    answer: Answer
    is_new: bool


class AddAnswer:
    def __init__(self, store: Store) -> None:
        self._store = store

    async def execute(self, dto: AddAnswerDTO) -> AddAnswerResultDTO:
        question_dto = QuestionDTO(text=dto.text, question_type=dto.question_type)
        question = await self._store.question.get(dto=question_dto)
        if question is None:
            question = await self._store.question.create(dto=question_dto)

        if dto.all_answers:
            group_dto = GroupDTO(
                question_id=question.question_id,
                all_answers=dto.all_answers,
                all_extra_answers=dto.all_extra_answers,
            )
            group = await self._store.group.get(dto=group_dto)
            if group is None:
                group = await self._store.group.create(dto=group_dto)
        else:
            group = None

        answer_dto = AnswerDTO(
            question_id=question.question_id,
            group_id=group.group_id if group else None,
            answer=dto.answer,
            is_correct=dto.is_correct,
        )
        answer = await self._store.answer.get(dto=answer_dto)
        if answer is None:
            answer = await self._store.answer.create(dto=answer_dto)
            is_new = True
        else:
            is_new = False

        return AddAnswerResultDTO(
            question=question, group=group, answer=answer, is_new=is_new
        )
