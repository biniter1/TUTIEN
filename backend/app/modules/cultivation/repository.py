from uuid import UUID

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
