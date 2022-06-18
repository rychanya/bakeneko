import uuid
from enum import Enum

from sqlalchemy import ARRAY, Column, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import ENUM, UUID

from bakeneko.db import Base


class TypeEnum(str, Enum):
    ONE = "ONE"
    MANY = "MANY"

class Question(Base):
    __tablename__ = "question"
    __table_args__ = (UniqueConstraint("text", "all_answers"),)
    question_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    question_type = Column(ENUM(TypeEnum), nullable=False)
    text = Column(String, nullable=False)
    all_answers = Column(ARRAY(String))
