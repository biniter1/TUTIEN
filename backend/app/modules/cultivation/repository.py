from uuid import UUID

from sqlalchemy.orm import Session

from app.modules.cultivation.models import CultivationProfile


def find_by_user_id(db: Session, user_id: UUID) -> CultivationProfile | None:
    return db.query(CultivationProfile).filter(CultivationProfile.user_id == user_id).first()


def add_profile(db: Session, profile: CultivationProfile) -> CultivationProfile:
    db.add(profile)
    db.flush()
    return profile
