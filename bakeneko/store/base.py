from typing import Protocol

from .exception import (
    DuplicatedAnswerError,
    DuplicatedGroupError,
    DuplicatedQuestionError,
)
from .types import Answer, AnswerDTO, Group, GroupDTO, IDType, Question, QuestionDTO


class AnswerStore(Protocol):
    async def get_by_id(self, answer_id: IDType) -> Answer | None:
        pass

    async def get(self, dto: AnswerDTO) -> Answer | None:
        pass

    async def create(self, dto: AnswerDTO) -> Answer:
        raise DuplicatedAnswerError


class GroupStore(Protocol):
    async def get_by_id(self, group_id: IDType) -> Group | None:
        pass

    async def get(self, dto: GroupDTO) -> Group | None:
        pass

    async def create(self, dto: GroupDTO) -> Group:
        raise DuplicatedGroupError


class QuestionStore(Protocol):
    async def get_by_id(self, question_id: IDType) -> Question | None:
        pass

    async def get(self, dto: QuestionDTO) -> Question | None:
        pass

    async def create(self, dto: QuestionDTO) -> Question:
        raise DuplicatedQuestionError


class Store(Protocol):
    answer: AnswerStore
    group: GroupStore
    question: QuestionStore
