from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from bakeneko.db.scheme import QuestionORM
from bakeneko.models.question import Question, QuestionInDB


def get_or_create(engine, question: Question) -> tuple[bool, QuestionInDB]:
    with Session(engine) as session:
        result = (
            session.execute(
                select(QuestionORM).where(
                    QuestionORM.question_type == question.question_type,
                    QuestionORM.text == question.text,
                    and_(
                        QuestionORM.all_answers.op("@>")(question.all_answers),
                        QuestionORM.all_answers.op("<@")(question.all_answers),
                    ),
                    and_(
                        QuestionORM.all_extra_answers.op("@>")(
                            question.all_extra_answers
                        ),
                        QuestionORM.all_extra_answers.op("<@")(
                            question.all_extra_answers
                        ),
                    ),
                )
            )
            .scalars()
            .first()
        )
        if result is None:
            question_orm = QuestionORM(
                question_type=question.question_type,
                text=question.text,
                all_answers=question.all_answers,
                all_extra_answers=question.all_extra_answers,
            )
            session.add(question_orm)
            session.commit()
            return True, QuestionInDB.from_orm(question_orm)
        else:
            return False, QuestionInDB.from_orm(result)
