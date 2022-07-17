from pydantic import UUID4
from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from bakeneko.db.scheme import QuestionORM
from bakeneko.models.question import Question, QuestionInDB


def get_from_model(session: Session, question: Question) -> None | QuestionORM:
    return (
        session.execute(
            select(QuestionORM).where(
                QuestionORM.question_type == question.question_type,
                QuestionORM.text == question.text,
                and_(
                    QuestionORM.all_answers.op("@>")(question.all_answers),
                    QuestionORM.all_answers.op("<@")(question.all_answers),
                ),
                and_(
                    QuestionORM.all_extra_answers.op("@>")(question.all_extra_answers),
                    QuestionORM.all_extra_answers.op("<@")(question.all_extra_answers),
                ),
            )
        )
        .scalars()
        .first()
    )


def create(session: Session, question: Question) -> QuestionORM:
    question_orm = QuestionORM(
        question_type=question.question_type,
        text=question.text,
        all_answers=question.all_answers,
        all_extra_answers=question.all_extra_answers,
    )
    session.add(question_orm)
    return question_orm


def _get_or_create(session: Session, question: Question) -> tuple[bool, QuestionORM]:
    question_orm = get_from_model(session=session, question=question)
    if question_orm is None:
        question_orm = create(session=session, question=question)
        session.flush()
        return True, question_orm
    else:
        return False, question_orm


def get_or_create(session: Session, question: Question) -> tuple[bool, QuestionInDB]:
    is_new, question_orm = _get_or_create(session=session, question=question)
    session.commit()
    return is_new, QuestionInDB.from_orm(question_orm)


def get_by_id(session: Session, _id: UUID4) -> QuestionInDB | None:
    result = session.get(QuestionORM, _id)
    if result is not None:
        return QuestionInDB.from_orm(result)


def search(session: Session, q: str) -> list[QuestionORM]:
    return (
        session.execute(select(QuestionORM).where(QuestionORM.text.ilike(f"%{q}%")))
        .scalars()
        .all()
    )
