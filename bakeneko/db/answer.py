from pydantic import UUID4
from sqlalchemy.orm import Session

from bakeneko.db.scheme import QuestionORM
from bakeneko.models.answer import Answer


def add_answer(engine, question_id: UUID4, answer: Answer):
    with Session(engine) as session:
        question: QuestionORM | None = session.get(QuestionORM, question_id)
        if question is None:
            raise ValueError
