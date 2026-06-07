from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.modules.cultivation.models import CultivationProfile


def find_by_user_id(db: Session, user_id: UUID) -> CultivationProfile | None:
    return db.query(CultivationProfile).filter(CultivationProfile.user_id == user_id).first()


def add_profile(db: Session, profile: CultivationProfile) -> CultivationProfile:
    db.add(profile)
    db.flush()
    return profile


def add_power(db: Session, user_id: UUID, amount: int) -> CultivationProfile | None:
    profile = find_by_user_id(db, user_id)
    if profile is None:
        return None
    profile.cultivation_power += amount
    return profile


def spend_spirit_energy(db: Session, user_id: UUID, amount: int) -> int:
    profile = find_by_user_id(db, user_id)
    if profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cultivation profile not found",
        )
    if profile.spirit_energy < amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Not enough spirit energy",
        )
    profile.spirit_energy -= amount  # mutation only after both checks pass
    return profile.spirit_energy


def add_reputation(db: Session, user_id: UUID, amount: int) -> CultivationProfile | None:
    profile = find_by_user_id(db, user_id)
    if profile is None:
        return None
    profile.reputation += amount
    return profile
