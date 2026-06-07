from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.modules.cultivation import repository as cultivation_repo
from app.modules.cultivation.models import CultivationProfile


def create_default_profile(db: Session, user_id: UUID) -> CultivationProfile:
    existing = cultivation_repo.find_by_user_id(db, user_id)
    if existing:
        return existing
    profile = CultivationProfile(user_id=user_id)
    return cultivation_repo.add_profile(db, profile)


def get_profile_by_user_id(db: Session, user_id: UUID) -> CultivationProfile | None:
    return cultivation_repo.find_by_user_id(db, user_id)


def add_cultivation_power(db: Session, user_id: UUID, amount: int) -> int:
    profile = cultivation_repo.add_power(db, user_id, amount)
    if profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cultivation profile not found",
        )
    return profile.cultivation_power


def spend_spirit_energy(db: Session, user_id: UUID, amount: int) -> int:
    return cultivation_repo.spend_spirit_energy(db, user_id, amount)


def add_reputation(db: Session, user_id: UUID, amount: int) -> int:
    profile = cultivation_repo.add_reputation(db, user_id, amount)
    if profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cultivation profile not found",
        )
    return profile.reputation
