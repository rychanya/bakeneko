import pytest

from bakeneko.db.question import get_or_create
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
def test_with_same_questions(
    engine, question_model_1: Question, question_model_2: Question
):
    is_new1, q1 = get_or_create(engine, question=question_model_1)
    is_new2, q2 = get_or_create(engine, question=question_model_2)

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
def test_with_one_questions(engine, question_model: Question):
    _, q = get_or_create(engine, question_model)

    assert question_model.question_type == q.question_type
    assert question_model.text == q.text
    assert set(question_model.all_answers) == set(q.all_answers)
    assert set(question_model.all_extra_answers) == set(q.all_extra_answers)
