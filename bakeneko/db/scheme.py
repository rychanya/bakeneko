import uuid

from sqlalchemy import ARRAY, Boolean, Column, ForeignKey, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import ENUM, UUID
from sqlalchemy.orm import declarative_base, relationship

from bakeneko.models.types import TypeEnum

Base = declarative_base()


class QuestionORM(Base):
    __tablename__ = "question"
    __table_args__ = (
        UniqueConstraint("question_type", "text", "all_answers", "all_extra_answers"),
    )
    question_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    question_type = Column(ENUM(TypeEnum), nullable=False)
    text = Column(String, nullable=False)
    all_answers = Column(ARRAY(String), nullable=False)
    all_extra_answers = Column(ARRAY(String), nullable=False)

    answers = relationship(
        "AnswerORM",
        back_populates="question",
        cascade="all, delete",
        passive_deletes=True,
    )


class AnswerORM(Base):
    __tablename__ = "answer"
    __table_args__ = (
        UniqueConstraint("question_id", "is_correct", "answer", "extra_answer"),
    )

    answer_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    question_id = Column(
        UUID(as_uuid=True), ForeignKey("question.question_id", ondelete="CASCADE")
    )
    is_correct = Column(Boolean(), nullable=False)
    answer = Column(ARRAY(String), nullable=False)
    extra_answer = Column(ARRAY(String), nullable=False)

    question = relationship("QuestionORM", back_populates="answers")
