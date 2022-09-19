import pytest

from bakeneko.models.store_dto import AnswerDTO, InsertDTO, QuestionDTO, SearchParams
from bakeneko.store.SQLStore import SQLStore

pytestmark = pytest.mark.anyio


async def test_insert_in_clear_db(store: SQLStore, question_dto: QuestionDTO):
    result = await store.insert_question(question_dto=question_dto)
    assert result is not None

    another_question_text = "another_text"
    assert question_dto.text != another_question_text
    question_dto.text = another_question_text

    result_2 = await store.insert_question(question_dto=question_dto)
    assert result_2 is not None


async def test_insert_twice(store: SQLStore, question_dto: QuestionDTO):
    result = await store.insert_question(question_dto=question_dto)
    assert result is not None

    result = await store.insert_question(question_dto=question_dto)
    assert result is None


async def test_insert_with_reverse_answers(store: SQLStore, question_dto: QuestionDTO):
    question_dto.all_answers = ["1", "2", "3"]
    result = await store.insert_question(question_dto=question_dto)
    assert result is not None

    result = await store.insert_question(question_dto=question_dto)
    assert result is None

    question_dto.all_answers.reverse()
    result = await store.insert_question(question_dto=question_dto)
    assert result is not None


async def test_insert_answer(
    store: SQLStore, question_dto: QuestionDTO, get_answer_dto
):
    question = await store.insert_question(question_dto)
    assert question is not None
    answer_dto: AnswerDTO = get_answer_dto(question.id_)
    answer = await store.insert_answer(answer_dto=answer_dto, question_id=question.id_)
    assert answer is not None
    assert question.id_ == answer.question_id
    fresh_question = await store.get_question_by_id(question.id_)
    assert fresh_question is not None
    assert fresh_question.answers[0] == answer


async def test_insert_qa(store: SQLStore, question_with_answer_dto: InsertDTO):
    result = await store.insert(question_with_answer=question_with_answer_dto)
    assert result


async def test_search(store: SQLStore, question_with_answer_dto: InsertDTO):
    result = await store.insert(question_with_answer=question_with_answer_dto)

    search_result = await store.search(SearchParams(q="Text"))

    assert search_result[0].id_ == result.question.id_
