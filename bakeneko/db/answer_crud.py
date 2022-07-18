from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from bakeneko.db import question_crud
from bakeneko.db.scheme import AnswerORM, QuestionORM
from bakeneko.models.add_answer import AddAnswer, AddAnswerResponse
from bakeneko.models.answer import AnswerInDB, BaseAnswer
from bakeneko.models.question import QuestionInDB


def get_by_model(session: Session, answer: BaseAnswer, question_id) -> None | AnswerORM:
    return (
        session.execute(
            select(AnswerORM).where(
                AnswerORM.question_id == question_id,
                AnswerORM.is_correct == answer.is_correct,
                and_(
                    AnswerORM.answer.op("@>")(answer.answer),
                    AnswerORM.answer.op("<@")(answer.answer),
                ),
                and_(
                    AnswerORM.extra_answer.op("@>")(answer.extra_answer),
                    AnswerORM.extra_answer.op("<@")(answer.extra_answer),
                ),
            )
        )
        .scalars()
        .first()
    )


def create(session: Session, answer: BaseAnswer, question_orm: QuestionORM):
    answer_orm = AnswerORM(
        question_id=question_orm.question_id,
        is_correct=answer.is_correct,
        answer=answer.answer,
        extra_answer=answer.extra_answer,
    )
    session.add(answer_orm)
    return answer_orm


def add_answer(session: Session, dto: AddAnswer) -> AddAnswerResponse:
    is_new_question, question_orm = question_crud._get_or_create(
        session=session, question=dto
    )
    answer_orm = get_by_model(
        session=session, answer=dto.answer, question_id=question_orm.question_id
    )
    if answer_orm is None:
        answer_orm = create(
            session=session, answer=dto.answer, question_orm=question_orm
        )
        session.commit()
        return AddAnswerResponse(
            is_new_question=is_new_question,
            question=QuestionInDB.from_orm(question_orm),
            is_new_answer=True,
            answer=AnswerInDB.from_orm(answer_orm),
        )
    else:
        return AddAnswerResponse(
            is_new_question=is_new_question,
            question=QuestionInDB.from_orm(question_orm),
            is_new_answer=False,
            answer=AnswerInDB.from_orm(answer_orm),
        )
