from abc import ABC

from bakeneko.models import Answer, AnswerDB

emoji_dict = {True: "🟢", False: "🔴", None: "⚪"}


async def search(q: str):
    return [
        {
            "id": "1",
            "title": "title",
            "type": "type",
            "answers": ["1", "2", "3"],
        },
        {
            "id": "2",
            "title": "title",
            "type": "type",
            "answers": ["1", "2", "3"],
        },
        {
            "id": "3",
            "title": "title",
            "type": "type",
            "answers": ["1", "2", "3"],
        },
        {
            "id": "4",
            "title": "title",
            "type": "type",
            "answers": ["1", "2", "3"],
        },
    ]


async def get_answer_by_id(answer_id):
    return {
        "id": answer_id,
        "title": "title",
        "type": "type",
        "answers": ["1", "2", "3"],
    }


class AnswerStore(ABC):  # pragma: no cover
    items_for_page = 10

    def insert(self, answer: Answer, user_id: str) -> tuple[AnswerDB, bool]:
        ...

    def get(self, answer_id: str) -> AnswerDB | None:
        ...

    def search(
        self, q: str, only_correct: bool = True, page: int = 1
    ) -> list[AnswerDB]:
        ...
