import pytest

from bakeneko.db import session_factory
from bakeneko.db.answer_crud import add_answer
from bakeneko.models.add_answer import AddAnswer


@pytest.mark.usefixtures("clear_db")
def test_correct():
    dto = AddAnswer.parse_obj(
        {
            "question_type": "ONE",
            "text": "NotEmptyString",
            "all_answers": [],
            "all_extra_answers": [],
            "answer": {"is_correct": True, "answer": ["1"], "extra_answer": []},
        }
    )
    with session_factory() as session:
        response1 = add_answer(session=session, dto=dto)
    assert response1.is_new_question is True
    assert response1.is_new_answer is True

    with session_factory() as session:
        response2 = add_answer(session=session, dto=dto)

    assert response2.is_new_question is False
    assert response2.is_new_answer is False
