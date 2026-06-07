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


def find_achievement_definition_by_code(
    db: Session, code: str
) -> AchievementDefinition | None:
    return (
        db.query(AchievementDefinition)
        .filter(AchievementDefinition.code == code)
        .first()
    )


def find_user_achievement(
    db: Session, user_id: UUID, achievement_id: UUID
) -> UserAchievement | None:
    return (
        db.query(UserAchievement)
        .filter(
            UserAchievement.user_id == user_id,
            UserAchievement.achievement_id == achievement_id,
        )
        .first()
    )


def create_user_achievement(
    db: Session, user_achievement: UserAchievement
) -> UserAchievement:
    db.add(user_achievement)
    db.flush()
    return user_achievement


def find_title_definition_by_code(db: Session, code: str) -> TitleDefinition | None:
    return (
        db.query(TitleDefinition)
        .filter(TitleDefinition.code == code)
        .first()
    )


def find_user_title(
    db: Session, user_id: UUID, title_id: UUID
) -> UserTitle | None:
    return (
        db.query(UserTitle)
        .filter(
            UserTitle.user_id == user_id,
            UserTitle.title_id == title_id,
        )
        .first()
    )


def create_user_title(db: Session, user_title: UserTitle) -> UserTitle:
    db.add(user_title)
    db.flush()
    return user_title
