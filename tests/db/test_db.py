import pytest
from sqlalchemy.engine import Engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from bakeneko.db import Base
from bakeneko.db.models import Question, TypeEnum


def test_fff(engine: Engine):
    with engine.connect() as con:
        Base.metadata.create_all(engine)
        # con.commit()

    with Session(engine) as session:
        q1 = Question(text="1", all_answers=["1", "2"], question_type=TypeEnum.ONE)
        session.add(q1)
        session.commit()
        print("#" * 10)
        print(q1.question_id)
        print("#" * 10)

    # assert False

    # with pytest.raises(IntegrityError):
    #     with Session(e) as session:
    #         q1 = Question(text="1", all_answers=["1", "2"])
    #         session.add(q1)
    #         session.commit()
