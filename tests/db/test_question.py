from uuid import uuid4

import pytest

from bakeneko.db import session_factory
from bakeneko.db.question_crud import get_by_id, get_or_create, search
from bakeneko.db.scheme import QuestionORM
from bakeneko.models.question import Question
from bakeneko.models.types import TypeEnum


@pytest.mark.usefixtures("clear_db")
@pytest.mark.parametrize(
    "question_model_1, question_model_2",
    [
        (
            Question(**{"question_type": TypeEnum.ONE, "text": "text"}),
            Question(**{"question_type": TypeEnum.ONE, "text": "text"}),
        ),
        (
            Question(
                **{
                    "question_type": TypeEnum.ONE,
                    "text": "text",
                    "all_answers": ["1", "2"],
                }
            ),
            Question(
                **{
                    "question_type": TypeEnum.ONE,
                    "text": "text",
                    "all_answers": ["2", "1"],
                }
            ),
        ),
        (
            Question(
                **{
                    "question_type": TypeEnum.MATCH,
                    "text": "text",
                    "all_answers": ["1", "2"],
                    "all_extra_answers": ["a", "b"],
                }
            ),
            Question(
                **{
                    "question_type": TypeEnum.MATCH,
                    "text": "text",
                    "all_answers": ["2", "1"],
                    "all_extra_answers": ["b", "a"],
                }
            ),
        ),
    ],
)
def test_with_same_questions(question_model_1: Question, question_model_2: Question):
    with session_factory() as session:
        is_new1, q1 = get_or_create(session, question=question_model_1)
        is_new2, q2 = get_or_create(session, question=question_model_2)

    assert is_new1 is True
    assert is_new2 is False
    assert q1.question_id == q2.question_id
    assert q1.question_type == q2.question_type
    assert q1.text == q2.text
    assert set(q1.all_answers) == set(q2.all_answers)
    assert set(q1.all_extra_answers) == set(q2.all_extra_answers)


@pytest.mark.usefixtures("clear_db")
@pytest.mark.parametrize(
    "question_model",
    [
        Question(**{"question_type": TypeEnum.ONE, "text": "text"}),
        Question(
            **{
                "question_type": TypeEnum.ONE,
                "text": "text",
                "all_answers": ["1", "2"],
            }
        ),
        Question(
            **{
                "question_type": TypeEnum.MATCH,
                "text": "text",
                "all_answers": ["1", "2"],
                "all_extra_answers": ["a", "b"],
            }
        ),
    ],
)
def test_with_one_questions(question_model: Question):
    with session_factory() as session:
        _, q = get_or_create(session, question_model)

    assert question_model.question_type == q.question_type
    assert question_model.text == q.text
    assert set(question_model.all_answers) == set(q.all_answers)
    assert set(question_model.all_extra_answers) == set(q.all_extra_answers)


@pytest.mark.usefixtures("clear_db")
def test_get_by_id():
    with session_factory() as session:
        q1 = get_by_id(session, uuid4())

    assert q1 is None

    with session_factory() as session:
        _, q2 = get_or_create(
            session, Question(**{"question_type": TypeEnum.ONE, "text": "text"})
        )

    with session_factory() as session:
        q3 = get_by_id(session, q2.question_id)

    assert q3 == q2


@pytest.mark.usefixtures("clear_db")
def test_search():
    question1 = QuestionORM(
        question_type="ONE", text="все коты", all_answers=[], all_extra_answers=[]
    )
    with session_factory() as session:
        session.add(question1)
        session.commit()

    with session_factory() as session:
        question_list = search(session, "все кот")

    assert question1.question_id == question_list[0].question_id
