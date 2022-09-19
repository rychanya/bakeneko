import abc
from uuid import UUID

from bakeneko.models import store_dto


class BaseStore(abc.ABC):  # pragma: no cover
    @abc.abstractmethod
    def __init__(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def setup(self):
        raise NotImplementedError

    @abc.abstractmethod
    async def insert_question(
        self, question_dto: store_dto.QuestionDTO
    ) -> store_dto.QuestionDTOWithID | None:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_question_by_id(self, id_: UUID) -> store_dto.QuestionDTOWithID | None:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_all_question(self) -> list[store_dto.QuestionDTOWithID]:
        raise NotImplementedError

    @abc.abstractmethod
    async def insert_answer(
        self, answer_dto: store_dto.AnswerDTO, question_id: UUID
    ) -> store_dto.AnswerDTOWithID | None:
        raise NotImplementedError

    @abc.abstractmethod
    async def insert(
        self, question_with_answer: store_dto.InsertDTO
    ) -> store_dto.InsertResultDTO:
        raise NotImplementedError

    @abc.abstractmethod
    async def search(
        self, params: store_dto.SearchParams
    ) -> list[store_dto.QuestionDTOWithID]:
        raise NotImplementedError
