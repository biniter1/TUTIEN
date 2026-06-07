from uuid import UUID

from sqlalchemy.orm import Session

from app.modules.achievements.models import (
    AchievementDefinition,
    TitleDefinition,
    UserAchievement,
    UserTitle,
)


def list_active_achievement_definitions(db: Session) -> list[AchievementDefinition]:
    return (
        db.query(AchievementDefinition)
        .filter(AchievementDefinition.is_active.is_(True))
        .all()
    )


def list_user_achievements(db: Session, user_id: UUID) -> list[UserAchievement]:
    return (
        db.query(UserAchievement)
        .filter(UserAchievement.user_id == user_id)
        .all()
    )


def list_active_title_definitions(db: Session) -> list[TitleDefinition]:
    return (
        db.query(TitleDefinition)
        .filter(TitleDefinition.is_active.is_(True))
        .all()
    )


def list_user_titles(db: Session, user_id: UUID) -> list[UserTitle]:
    return (
        db.query(UserTitle)
        .filter(UserTitle.user_id == user_id)
        .all()
    )
