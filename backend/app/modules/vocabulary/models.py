import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.database import Base


class VocabularySet(Base):
    __tablename__ = "vocabulary_sets"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    theme = Column(String, nullable=True)
    difficulty = Column(String, default="beginner", nullable=False)
    required_realm = Column(String, nullable=True)
    total_words = Column(Integer, default=0, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    words = relationship("VocabularyWord", back_populates="set")


class VocabularyWord(Base):
    __tablename__ = "vocabulary_words"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    set_id = Column(
        UUID(as_uuid=True),
        ForeignKey("vocabulary_sets.id"),
        index=True,
        nullable=False,
    )
    english = Column(String, nullable=False)
    vietnamese = Column(String, nullable=False)
    pronunciation = Column(String, nullable=True)
    example_sentence = Column(Text, nullable=True)
    example_translation = Column(Text, nullable=True)
    difficulty = Column(String, default="beginner", nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    set = relationship("VocabularySet", back_populates="words")
