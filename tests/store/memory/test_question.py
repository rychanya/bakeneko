from uuid import uuid4

import pytest

from bakeneko.store.exception import DuplicatedQuestionError
from bakeneko.store.in_memory import MemoryQuestionStore
from bakeneko.store.types import Question, QuestionDTO, QuestionType

pytestmark = pytest.mark.anyio


@pytest.fixture
def store():
    return MemoryQuestionStore()


@pytest.fixture
def dto():
    return QuestionDTO(text="text", question_type=QuestionType.ONE)


async def test_get(store: MemoryQuestionStore, dto: QuestionDTO):
    assert await store.get(dto) is None

    question_in_memory = Question(
        text=dto.text, question_type=dto.question_type, question_id=str(uuid4())
    )
    store._data.append(question_in_memory)

    assert await store.get(dto) == question_in_memory


async def test_get_by_id(store: MemoryQuestionStore, dto: QuestionDTO):
    question_id = str(uuid4())
    assert await store.get_by_id(question_id) is None

    question_in_memory = Question(
        text=dto.text, question_type=dto.question_type, question_id=question_id
    )
    store._data.append(question_in_memory)

    question = await store.get_by_id(question_id)
    assert question is not None
    assert question.question_id == question_id


async def test_create(store: MemoryQuestionStore, dto: QuestionDTO):
    assert await store.get(dto) is None

    question = await store.create(dto)
    assert question is not None
    assert await store.get(dto) == question

    with pytest.raises(DuplicatedQuestionError):
        await store.create(dto)
