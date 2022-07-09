import pytest
from pydantic import ValidationError

from bakeneko.models.add_answer import AddAnswer
from bakeneko.models.types import TypeEnum

valid_data = [
    {
        "question_type": TypeEnum.ONE,
        "text": "NotEmptyString",
        "all_answers": [],
        "all_extra_answers": [],
        "answer": {
            "is_correct": True,
            "answer": [
                "1",
            ],
            "extra_answer": [],
        },
    },
    {
        "question_type": TypeEnum.MATCH,
        "text": "NotEmptyString",
        "all_answers": [],
        "all_extra_answers": [],
        "answer": {
            "is_correct": True,
            "answer": ["1", "2"],
            "extra_answer": [],
        },
    },
    {
        "question_type": TypeEnum.MATCH,
        "text": "NotEmptyString",
        "all_answers": [],
        "all_extra_answers": [],
        "answer": {
            "is_correct": True,
            "answer": ["1", "2"],
            "extra_answer": ["a", "b"],
        },
    },
]
invalid_data = [
    # answer "1" not in all_answers
    {
        "question_type": TypeEnum.ONE,
        "text": "NotEmptyString",
        "all_answers": ["2", "3"],
        "all_extra_answers": [],
        "answer": {
            "is_correct": True,
            "answer": [
                "1",
            ],
            "extra_answer": [],
        },
    },
    {
        "question_type": TypeEnum.MANY,
        "text": "NotEmptyString",
        "all_answers": ["1", "2", "3"],
        "all_extra_answers": [],
        "answer": {
            "is_correct": True,
            "answer": ["1", "4"],
            "extra_answer": [],
        },
    },
    {
        "question_type": TypeEnum.ORDER,
        "text": "NotEmptyString",
        "all_answers": ["1", "2", "3"],
        "all_extra_answers": [],
        "answer": {
            "is_correct": True,
            "answer": ["1", "2"],
            "extra_answer": [],
        },
    },
    {
        "question_type": TypeEnum.ONE,
        "text": "NotEmptyString",
        "all_answers": [],
        "all_extra_answers": [],
        "answer": {
            "is_correct": True,
            "answer": ["1", "2"],
            "extra_answer": ["a", "b"],
        },
    },
    {
        "question_type": TypeEnum.MANY,
        "text": "NotEmptyString",
        "all_answers": [],
        "all_extra_answers": [],
        "answer": {
            "is_correct": True,
            "answer": ["1", "2"],
            "extra_answer": ["a", "b"],
        },
    },
    {
        "question_type": TypeEnum.ORDER,
        "text": "NotEmptyString",
        "all_answers": [],
        "all_extra_answers": [],
        "answer": {
            "is_correct": True,
            "answer": ["1", "2"],
            "extra_answer": ["a", "b"],
        },
    },
    {
        "question_type": TypeEnum.MATCH,
        "text": "NotEmptyString",
        "all_answers": [],
        "all_extra_answers": [],
        "answer": {
            "is_correct": True,
            "answer": ["1", "2"],
            "extra_answer": ["a", "b", "c"],
        },
    },
    {
        "question_type": TypeEnum.MATCH,
        "text": "NotEmptyString",
        "all_answers": ["1", "2"],
        "all_extra_answers": ["a", "b"],
        "answer": {
            "is_correct": True,
            "answer": ["1", "3"],
            "extra_answer": ["a", "b"],
        },
    },
    {
        "question_type": TypeEnum.MATCH,
        "text": "NotEmptyString",
        "all_answers": ["1", "2"],
        "all_extra_answers": ["a", "b"],
        "answer": {
            "is_correct": True,
            "answer": ["1", "2"],
            "extra_answer": ["a", "c"],
        },
    },
]


class TestAddAnswer:
    @pytest.mark.parametrize("data", valid_data)
    def test_valid(self, data):
        AddAnswer.parse_obj(data)

    @pytest.mark.parametrize("data", invalid_data)
    def test_invalid(self, data):
        with pytest.raises(ValidationError):
            AddAnswer.parse_obj(data)
