import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base


class CultivationProfile(Base):
    __tablename__ = "cultivation_profiles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        unique=True,
        index=True,
        nullable=False,
    )
    realm = Column(String, default="Pham Nhan", nullable=False)
    realm_stage = Column(String, nullable=True)
    cultivation_power = Column(Integer, default=0, nullable=False)
    spirit_energy = Column(Integer, default=100, nullable=False)
    max_spirit_energy = Column(Integer, default=100, nullable=False)
    reputation = Column(Integer, default=0, nullable=False)
    streak_days = Column(Integer, default=0, nullable=False)
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
