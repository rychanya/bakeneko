import typing
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from bakeneko.models import store_dto
from bakeneko.store.base import BaseStore
from bakeneko.store.SQLStore.db_models import Answers, Base, Questions


class SQLStore(BaseStore):
    def __init__(self, db_url: str, echo: bool) -> None:
        self._engine = create_async_engine(db_url, echo=echo)
        self._sessionmaker = sessionmaker(
            self._engine, expire_on_commit=False, class_=AsyncSession
        )
        self.session = lambda: typing.cast(AsyncSession, self._sessionmaker())

    async def setup(self):
        async with self._engine.begin() as connection:
            await connection.run_sync(Base.metadata.create_all)

    async def insert(
        self, question_with_answer: store_dto.InsertDTO
    ) -> store_dto.InsertResultDTO:
        async with self.session() as session:
            question_stmt = select(Questions).where(
                Questions.type == question_with_answer.type_,
                Questions.text == question_with_answer.text,
                Questions.all_answers == question_with_answer.all_answers,
                Questions.all_extra_answers == question_with_answer.all_extra_answers,
            )
            result = await session.execute(question_stmt)
            question_model: Questions | None = result.scalars().first()
            if question_model is None:
                question_model = Questions(
                    type=question_with_answer.type_,
                    text=question_with_answer.text,
                    all_answers=question_with_answer.all_answers,
                    all_extra_answers=question_with_answer.all_extra_answers,
                    answers=[],
                )
                session.add(question_model)
                await session.flush()
            answer_model = Answers(
                value=question_with_answer.value,
                is_correct=question_with_answer.is_correct,
            )
            question_model.answers.append(answer_model)
            await session.commit()
            return store_dto.InsertResultDTO(
                question=question_model.to_dto(),
                answer=answer_model.to_dto(),
                is_new=True,
            )

    async def insert_answer(
        self, answer_dto: store_dto.AnswerDTO, question_id: UUID
    ) -> store_dto.AnswerDTOWithID | None:
        async with self.session() as session:
            question_model: Questions | None = await session.get(Questions, question_id)
            if question_model is None:
                return
            answer_model = Answers.from_dto(answer_dto)
            question_model.answers.append(answer_model)
            await session.commit()
            return answer_model.to_dto()

    async def insert_question(
        self, question_dto: store_dto.QuestionDTO
    ) -> store_dto.QuestionDTOWithID | None:
        async with self.session() as session:
            try:
                question_model = Questions.from_dto(question_dto)
                session.add(question_model)
                await session.commit()
                return question_model.to_dto()
            except IntegrityError:
                await session.rollback()

    async def get_question_by_id(self, id_: UUID) -> store_dto.QuestionDTOWithID | None:
        async with self.session() as session:
            question_model: Questions | None = await session.get(Questions, ident=id_)
            if question_model is not None:
                return question_model.to_dto()

    async def search(
        self, params: store_dto.SearchParams
    ) -> list[store_dto.QuestionDTOWithID]:
        async with self.session() as session:
            search_stmt = select(Questions).where(Questions.text.ilike(f"%{params.q}%"))
            result = await session.execute(search_stmt)
            question_models: list[Questions] = result.unique().scalars().all()
            return [question.to_dto() for question in question_models]

    async def get_all_question(self) -> list[store_dto.QuestionDTOWithID]:
        async with self.session() as session:
            result = await session.execute(select(Questions))
            data: list[Questions] = result.unique().scalars().all()
            return [v.to_dto() for v in data]
