from pydantic import UUID4
from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from bakeneko.db.scheme import AnswerORM, QuestionORM
from bakeneko.models.answer import Answer, AnswerInDB
from bakeneko.models.question import QuestionInDB
from bakeneko.models.types import TypeEnum


def add_answer(engine, question_id: UUID4, answer: Answer):
    with Session(engine) as session:
        question_orm: QuestionORM | None = session.get(QuestionORM, question_id)
        if question_orm is None:
            raise ValueError
        question = QuestionInDB.from_orm(question_orm)

        match question.question_type:
            case TypeEnum.ONE:
                if len(answer.answer) != 1 or len(answer.extra_answer) != 0:
                    raise ValueError
                if question.all_answers and not set(question.all_answers).issuperset(
                    answer.answer
                ):
                    raise ValueError

            case TypeEnum.MANY:
                if len(answer.extra_answer) != 0:
                    raise ValueError
                if question.all_answers and not set(question.all_answers).issuperset(
                    answer.answer
                ):
                    raise ValueError

            case TypeEnum.ORDER:
                if len(answer.extra_answer) != 0:
                    raise ValueError
                if question.all_answers and (question.all_answers != answer.answer):
                    raise ValueError

            case TypeEnum.MATCH:
                if question.all_answers and not (
                    set(question.all_answers) == set(answer.answer)
                ):
                    raise ValueError
                if question.all_extra_answers and not (
                    set(question.all_extra_answers) == set(answer.extra_answer)
                ):
                    raise ValueError

        result: AnswerORM | None = (
            session.execute(
                select(AnswerORM).where(
                    AnswerORM.question_id == question_orm.question_id,
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
        if result is None:
            answer_orm = AnswerORM(
                is_correct=answer.is_correct,
                answer=answer.answer,
                extra_answer=answer.extra_answer,
            )
            question_orm.answers.append(answer_orm)
            session.commit()
            return True, AnswerInDB.from_orm(answer_orm)
        else:
            return False, AnswerInDB.from_orm(result)
