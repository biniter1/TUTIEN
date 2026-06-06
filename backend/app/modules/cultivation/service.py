from uuid import UUID

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
