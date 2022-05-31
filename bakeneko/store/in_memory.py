from uuid import uuid4

from .base import (
    Answer,
    AnswerDTO,
    DuplicatedAnswerError,
    DuplicatedGroupError,
    DuplicatedQuestionError,
    Group,
    GroupDTO,
    IDType,
    Question,
    QuestionDTO,
)


class MemoryQuestionStore:
    def __init__(self) -> None:
        self._data: list[Question] = []

    async def get_by_id(self, question_id: IDType) -> Question | None:
        for question in self._data:
            if question.question_id == question_id:
                return question

    async def get(self, dto: QuestionDTO) -> Question | None:
        for question in self._data:
            if (
                question.question_type == dto.question_type
                and question.text == question.text
            ):
                return question

    async def create(self, dto: QuestionDTO) -> Question | None:
        if await self.get(dto) is not None:
            raise DuplicatedQuestionError
        question = Question(
            text=dto.text, question_type=dto.question_type, question_id=str(uuid4())
        )
        self._data.append(question)
        return question


class MemoryGroupStore:
    def __init__(self) -> None:
        self._data: list[Group] = []

    async def get_by_id(self, group_id: IDType) -> Group | None:
        for group in self._data:
            if group.group_id == group_id:
                return group

    async def get(self, dto: GroupDTO) -> Group | None:
        for group in self._data:
            if (
                group.all_answers == dto.all_answers
                and group.all_extra_answers == group.all_extra_answers
                and group.question_id == dto.question_id
            ):
                return group

    async def create(self, dto: GroupDTO) -> Group:
        if await self.get(dto) is not None:
            raise DuplicatedGroupError
        group = Group(
            group_id=str(uuid4()),
            question_id=dto.question_id,
            all_answers=dto.all_answers,
            all_extra_answers=dto.all_extra_answers,
        )
        self._data.append(group)
        return group


class MemoryAnswerStore:
    def __init__(self) -> None:
        self._data: list[Answer] = []

    async def get_by_id(self, answer_id: IDType) -> Answer | None:
        for answer in self._data:
            if answer.answer_id == answer_id:
                return answer

    async def get(self, dto: AnswerDTO) -> Answer | None:
        for answer in self._data:
            if (
                answer.answer == dto.answer
                and answer.group_id == dto.group_id
                and answer.is_correct == dto.is_correct
                and answer.question_id == dto.question_id
            ):
                return answer

    async def create(self, dto: AnswerDTO) -> Answer:
        if await self.get(dto) is not None:
            raise DuplicatedAnswerError
        answer = Answer(
            answer_id=str(uuid4()),
            question_id=dto.question_id,
            group_id=dto.group_id,
            answer=dto.answer,
            is_correct=dto.is_correct,
        )
        self._data.append(answer)
        return answer


class MemoryStore:
    def __init__(self) -> None:
        self.answer = MemoryAnswerStore()
        self.group = MemoryGroupStore()
        self.question = MemoryQuestionStore()
