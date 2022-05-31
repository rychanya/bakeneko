from uuid import uuid4

import pytest

from bakeneko.store.exception import DuplicatedGroupError
from bakeneko.store.in_memory import MemoryGroupStore
from bakeneko.store.types import Group, GroupDTO

pytestmark = pytest.mark.anyio


@pytest.fixture
def store():
    return MemoryGroupStore()


@pytest.fixture
def dto():
    return GroupDTO(
        question_id=str(uuid4()),
        all_answers=frozenset(("1", "2")),
        all_extra_answers=frozenset(("e1", "e2")),
    )


async def test_get(store: MemoryGroupStore, dto: GroupDTO):
    assert await store.get(dto) is None

    group_in_memory = Group(
        group_id=str(uuid4()),
        question_id=dto.question_id,
        all_answers=dto.all_answers,
        all_extra_answers=dto.all_extra_answers,
    )
    store._data.append(group_in_memory)

    assert await store.get(dto) == group_in_memory


async def test_get_by_id(store: MemoryGroupStore, dto: GroupDTO):
    group_id = str(uuid4())
    assert await store.get_by_id(group_id) is None

    group_in_memory = Group(
        group_id=group_id,
        question_id=dto.question_id,
        all_answers=dto.all_answers,
        all_extra_answers=dto.all_extra_answers,
    )
    store._data.append(group_in_memory)

    group = await store.get_by_id(group_id)
    assert group is not None
    assert group.group_id == group_id


async def test_create(store: MemoryGroupStore, dto: GroupDTO):
    assert await store.get(dto) is None

    group = await store.create(dto)
    assert group is not None
    assert await store.get(dto) == group

    with pytest.raises(DuplicatedGroupError):
        await store.create(dto)
