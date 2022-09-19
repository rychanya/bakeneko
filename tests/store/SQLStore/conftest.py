import pytest

from bakeneko.models.enums import TypeEnumDB
from bakeneko.models.store_dto import AnswerDTO, InsertDTO, QuestionDTO
from bakeneko.store.SQLStore import SQLStore
from bakeneko.store.SQLStore.db_models import Base
from bakeneko.store.SQLStore.settings import settings
from tests.utils import AsyncPostgresContainer


@pytest.fixture(scope="session", autouse=True)
async def db_container():
    async with AsyncPostgresContainer():
        yield


@pytest.fixture
async def store():
    store = SQLStore(db_url=settings.db_url, echo=settings.echo)
    async with store._engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
    await store.setup()
    return store


@pytest.fixture
def question_dto():
    return QuestionDTO(
        type_=TypeEnumDB.ONE,
        text="question_1",
        all_answers=[],
        all_extra_answers=[],
        answers=[],
    )


@pytest.fixture
def get_answer_dto():
    return lambda question_id: AnswerDTO(
        question_id=question_id, value=["1"], is_correct=True
    )


@pytest.fixture
def question_with_answer_dto():
    return InsertDTO(
        type_=TypeEnumDB.ONE,
        text="text question",
        all_answers=[],
        all_extra_answers=[],
        value=["1"],
        is_correct=True,
    )
