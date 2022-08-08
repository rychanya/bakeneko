from uuid import uuid4

from bakeneko.models import Answer, AnswerDB
from bakeneko.store import AnswerStore


def answer_eq(answer: Answer, answer_db: AnswerDB):
    return all(
        [
            answer.question == answer_db.question,
            answer.type == answer_db.type,
            answer.all_answers == answer_db.all_answers,
            answer.all_extra_answers == answer_db.all_extra_answers,
            answer.answer == answer_db.answer,
            answer.extra_answer == answer_db.extra_answer,
            answer.is_correct == answer_db.is_correct,
        ]
    )


class MemoryAnswerStore(AnswerStore):
    def __init__(self) -> None:
        self._db = []

    def insert(self, answer: Answer, user_id: str) -> tuple[AnswerDB, bool]:
        for _answer in self._db:
            answer_db = AnswerDB.parse_obj(_answer)
            if answer_eq(answer=answer, answer_db=answer_db):
                return answer_db, False
        else:
            answer_dict = answer.dict()
            answer_dict["id"] = str(uuid4())
            answer_dict["by"] = user_id
            self._db.append(answer_dict)
            return AnswerDB.parse_obj(answer_dict), True

    def get(self, answer_id: str) -> AnswerDB | None:
        for answer in self._db:
            if answer.get("id") == answer_id:
                return AnswerDB.parse_obj(answer)

    def search(
        self, q: str, only_correct: bool = True, page: int = 1
    ) -> list[AnswerDB]:
        result: list[AnswerDB] = []
        for answer in self._db:
            if only_correct and answer.get("is_correct") is not True:
                continue
            if q.lower() in answer.get("question", "").lower():
                result.append(AnswerDB.parse_obj(answer))
        start = (page - 1) * self.items_for_page
        end = page * self.items_for_page
        return result[start:end]
