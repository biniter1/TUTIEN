from uuid import UUID

from sqlalchemy.orm import Session

from app.modules.achievements import repository as achievement_repo
from app.modules.achievements.schemas import (
    AchievementResponse,
    AchievementsResponse,
    TitleResponse,
    TitlesResponse,
)


def get_user_achievements(db: Session, user_id: UUID) -> AchievementsResponse:
    definitions = achievement_repo.list_active_achievement_definitions(db)
    user_achievements = achievement_repo.list_user_achievements(db, user_id)

    # Build lookup keyed by achievement_id for O(1) access
    unlocked_map = {ua.achievement_id: ua for ua in user_achievements}

    results: list[AchievementResponse] = []
    for defn in definitions:
        ua = unlocked_map.get(defn.id)
        is_unlocked = ua is not None

        # Hidden achievements are excluded from the response unless the user has unlocked them
        if defn.is_hidden and not is_unlocked:
            continue

        results.append(
            AchievementResponse(
                code=defn.code,
                name=defn.name,
                description=defn.description,
                category=defn.category,
                is_hidden=defn.is_hidden,
                is_unlocked=is_unlocked,
                unlocked_at=ua.unlocked_at if ua else None,
                reward_title_code=defn.reward_title_code,
            )
        )

    return AchievementsResponse(achievements=results)


def get_user_titles(db: Session, user_id: UUID) -> TitlesResponse:
    definitions = achievement_repo.list_active_title_definitions(db)
    user_titles = achievement_repo.list_user_titles(db, user_id)

    # Build lookup keyed by title_id for O(1) access
    unlocked_map = {ut.title_id: ut for ut in user_titles}

    results: list[TitleResponse] = []
    for defn in definitions:
        ut = unlocked_map.get(defn.id)
        is_unlocked = ut is not None

        results.append(
            TitleResponse(
                code=defn.code,
                name=defn.name,
                description=defn.description,
                rarity=defn.rarity,
                is_unlocked=is_unlocked,
                is_equipped=ut.is_equipped if ut else False,
                unlocked_at=ut.unlocked_at if ut else None,
            )
        )

    return TitlesResponse(titles=results)
