from uuid import uuid4

import pytest

from bakeneko.store.exception import DuplicatedAnswerError
from bakeneko.store.in_memory import MemoryAnswerStore
from bakeneko.store.types import Answer, AnswerDTO

pytestmark = pytest.mark.anyio


@pytest.fixture
def store():
    return MemoryAnswerStore()


@pytest.fixture
def dto():
    return AnswerDTO(
        question_id=str(uuid4()), group_id=None, answer=("1", "2"), is_correct=None
    )


async def test_get(store: MemoryAnswerStore, dto: AnswerDTO):
    assert await store.get(dto) is None

    answer_in_memory = Answer(
        answer_id=str(uuid4()),
        question_id=dto.question_id,
        group_id=dto.group_id,
        answer=dto.answer,
        is_correct=dto.is_correct,
    )
    store._data.append(answer_in_memory)

    assert await store.get(dto) == answer_in_memory


async def test_get_by_id(store: MemoryAnswerStore, dto: AnswerDTO):
    answer_id = str(uuid4())
    assert await store.get_by_id(answer_id) is None

    answer_in_memory = Answer(
        answer_id=answer_id,
        question_id=dto.question_id,
        group_id=dto.group_id,
        answer=dto.answer,
        is_correct=dto.is_correct,
    )
    store._data.append(answer_in_memory)
    print(store._data)
    answer = await store.get_by_id(answer_id)
    assert answer is not None
    assert answer.answer_id == answer_id


async def test_create(store: MemoryAnswerStore, dto: AnswerDTO):
    assert await store.get(dto) is None

    answer = await store.create(dto)
    assert answer is not None
    assert await store.get(dto) == answer

    with pytest.raises(DuplicatedAnswerError):
        await store.create(dto)
