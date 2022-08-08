import pytest

from bakeneko.models import Answer
from bakeneko.store import AnswerStore
from bakeneko.store.memory import MemoryAnswerStore


@pytest.mark.parametrize("store", [MemoryAnswerStore()])
def test_insert_twice(store: AnswerStore):
    answer = Answer.parse_obj(
        {
            "question": "question",
            "type": "ONE",
            "all_answers": [],
            "all_extra_answers": [],
            "answer": ["1"],
            "extra_answer": [],
            "is_correct": True,
        },
    )

    answer_db_1, is_new_1 = store.insert(answer=answer, user_id="fake")
    assert is_new_1 is True
    answer_db_2, is_new_2 = store.insert(answer=answer, user_id="fake")
    assert is_new_2 is False
    assert answer_db_1 == answer_db_2


@pytest.mark.parametrize("store", [MemoryAnswerStore()])
def test_insert_answer_ordering_many_type(store: AnswerStore):
    answer_1 = Answer.parse_obj(
        {
            "question": "question",
            "type": "MANY",
            "all_answers": [],
            "all_extra_answers": [],
            "answer": ["1", "2"],
            "extra_answer": [],
            "is_correct": True,
        },
    )
    answer_2 = Answer.parse_obj(
        {
            "question": "question",
            "type": "MANY",
            "all_answers": [],
            "all_extra_answers": [],
            "answer": ["2", "1"],
            "extra_answer": [],
            "is_correct": True,
        },
    )

    answer_db_1, is_new_1 = store.insert(answer=answer_1, user_id="fake")
    assert is_new_1 is True
    answer_db_2, is_new_2 = store.insert(answer=answer_2, user_id="fake")
    assert is_new_2 is False
    assert answer_db_1 == answer_db_2
