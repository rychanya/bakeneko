import uuid

from sqlalchemy import ARRAY, Column, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import ENUM, UUID
from sqlalchemy.orm import declarative_base

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
