import typing
from uuid import UUID as UUID_PY_TYPE
from uuid import uuid4

from sqlalchemy import ARRAY, Boolean, Column, ForeignKey, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import ENUM, UUID
from sqlalchemy.orm import declarative_base, relationship

from bakeneko.models.enums import TypeEnumDB
from bakeneko.models.store_dto import (
    AnswerDTO,
    AnswerDTOWithID,
    QuestionDTO,
    QuestionDTOWithID,
)

Base = declarative_base()


class Questions(Base):
    __tablename__ = "questions"
    __table_args__ = (
        UniqueConstraint("type", "text", "all_answers", "all_extra_answers"),
    )
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    type = Column(ENUM(TypeEnumDB))
    text = Column(String)
    all_answers = Column(ARRAY(String))
    all_extra_answers = Column(ARRAY(String))
    answers = relationship("Answers", lazy=False)

    @staticmethod
    def from_dto(dto: QuestionDTO) -> "Questions":
        return Questions(
            type=dto.type_,
            text=dto.text,
            all_answers=dto.all_answers,
            all_extra_answers=dto.all_extra_answers,
            answers=[],
        )

    def to_dto(self) -> QuestionDTOWithID:
        return QuestionDTOWithID(
            id_=typing.cast(UUID_PY_TYPE, self.id),
            type_=typing.cast(TypeEnumDB, self.type),
            text=typing.cast(str, self.text),
            all_answers=typing.cast(list[str], self.all_answers),
            all_extra_answers=typing.cast(list[str], self.all_extra_answers),
            answers=[answer.to_dto() for answer in self.answers],
        )


class Answers(Base):
    __tablename__ = "answers"
    __table_args__ = (UniqueConstraint("question_id", "value", "is_correct"),)
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    question_id = Column(UUID(as_uuid=True), ForeignKey("questions.id"), nullable=False)
    value = Column(ARRAY(String))
    is_correct = Column(Boolean)

    @staticmethod
    def from_dto(dto: AnswerDTO) -> "Answers":
        return Answers(
            question_id=dto.question_id, value=dto.value, is_correct=dto.is_correct
        )

    def to_dto(self) -> AnswerDTOWithID:
        return AnswerDTOWithID(
            id_=typing.cast(UUID_PY_TYPE, self.id),
            question_id=typing.cast(UUID_PY_TYPE, self.question_id),
            value=typing.cast(list[str], self.value),
            is_correct=typing.cast(bool, self.is_correct),
        )
