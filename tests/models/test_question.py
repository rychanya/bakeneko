import uuid

import pytest
from pydantic import ValidationError

from bakeneko.models.question import QuestionInDB
from bakeneko.models.types import TypeEnum


@pytest.fixture
def base_question_data():
    return {
        "text": "NotEmptyString",
        "question_id": uuid.uuid4(),
    }


@pytest.fixture
def base_match_question_data():
    return {
        "question_type": TypeEnum.MATCH,
        "text": "NotEmptyString",
        "question_id": uuid.uuid4(),
    }


@pytest.mark.parametrize("question_type", list(TypeEnum))
def test_base_correct_data(base_question_data: dict, question_type):
    base_question_data["question_type"] = question_type
    QuestionInDB(**base_question_data)


@pytest.mark.parametrize("question_type", list(TypeEnum))
def test_base_empty_text(base_question_data: dict, question_type):
    base_question_data["question_type"] = question_type

    with pytest.raises(ValidationError):
        base_question_data["text"] = ""
        QuestionInDB(**base_question_data)

    with pytest.raises(ValidationError):
        del base_question_data["text"]
        QuestionInDB(**base_question_data)


@pytest.mark.parametrize("question_type", list(TypeEnum))
def test_base_not_uuid(base_question_data: dict, question_type):
    base_question_data["question_type"] = question_type

    with pytest.raises(ValidationError):
        base_question_data["question_id"] = ""
        QuestionInDB(**base_question_data)

    with pytest.raises(ValidationError):
        base_question_data["question_id"] = "not uuid"
        QuestionInDB(**base_question_data)

    with pytest.raises(ValidationError):
        del base_question_data["question_id"]
        QuestionInDB(**base_question_data)


@pytest.mark.parametrize("question_type", list(TypeEnum))
@pytest.mark.parametrize("all_answers", [[], ["1", "2"]])
def test_all_answers(base_question_data, question_type, all_answers):
    base_question_data["question_type"] = question_type
    base_question_data["all_answers"] = all_answers
    QuestionInDB(**base_question_data)


@pytest.mark.parametrize("question_type", list(TypeEnum))
@pytest.mark.parametrize(
    "all_answers",
    [
        ["1", "1"],
        [1, "3"],
        [
            "1",
        ],
    ],
)
def test_all_answers_incorrect(base_question_data, question_type, all_answers):
    base_question_data["question_type"] = question_type
    base_question_data["all_answers"] = all_answers
    with pytest.raises(ValidationError):
        QuestionInDB(**base_question_data)


@pytest.mark.parametrize(
    "all_answers, all_extra_answers",
    [
        ([], []),
        (None, None),
        (None, []),
        ([], None),
        (["1", "2"], ["a", "b"]),
        (["1", "2"], None),
    ],
)
def test_match_correct_data(base_match_question_data, all_answers, all_extra_answers):
    if all_answers is not None:
        base_match_question_data["all_answers"] = all_answers
    if all_extra_answers is not None:
        base_match_question_data["all_extra_answers"] = all_extra_answers
    QuestionInDB(**base_match_question_data)


@pytest.mark.parametrize(
    "all_answers, all_extra_answers",
    [
        (["1", "2"], ["a", "b", "c"]),
        (None, ["a", "b"]),
        (
            ["1", "2"],
            [
                "a",
            ],
        ),
    ],
)
def test_match_raises(base_match_question_data, all_answers, all_extra_answers):
    if all_answers is not None:
        base_match_question_data["all_answers"] = all_answers
    if all_extra_answers is not None:
        base_match_question_data["all_extra_answers"] = all_extra_answers
    with pytest.raises(ValidationError):
        QuestionInDB(**base_match_question_data)
