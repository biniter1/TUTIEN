from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy.orm import Session

from app.modules.achievements import repository as achievement_repo
from app.modules.achievements.models import UserAchievement, UserTitle
from app.modules.achievements.schemas import (
    AchievementResponse,
    AchievementUnlockResult,
    AchievementsResponse,
    TitleResponse,
    TitlesResponse,
    UnlockedAchievementInfo,
    UnlockedTitleInfo,
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


# ---------------------------------------------------------------------------
# Unlock helpers — all flush only; caller owns db.commit()
# ---------------------------------------------------------------------------

def _grant_title_by_code(
    db: Session, user_id: UUID, title_code: str, unlocked_at: datetime
) -> UnlockedTitleInfo | None:
    title_def = achievement_repo.find_title_definition_by_code(db, title_code)
    if title_def is None or not title_def.is_active:
        return None  # missing or inactive title — silent no-op

    existing = achievement_repo.find_user_title(db, user_id, title_def.id)
    if existing is not None:
        return None  # already granted — idempotent

    user_title = UserTitle(user_id=user_id, title_id=title_def.id, unlocked_at=unlocked_at)
    achievement_repo.create_user_title(db, user_title)
    return UnlockedTitleInfo(code=title_def.code, name=title_def.name, rarity=title_def.rarity)


def unlock_achievement_by_code(
    db: Session, user_id: UUID, achievement_code: str
) -> AchievementUnlockResult:
    achievement_def = achievement_repo.find_achievement_definition_by_code(db, achievement_code)
    if achievement_def is None or not achievement_def.is_active:
        return AchievementUnlockResult()  # missing or inactive — silent no-op

    existing_ua = achievement_repo.find_user_achievement(db, user_id, achievement_def.id)
    if existing_ua is not None:
        return AchievementUnlockResult()  # already unlocked — idempotent

    now = datetime.now(timezone.utc)
    user_achievement = UserAchievement(
        user_id=user_id, achievement_id=achievement_def.id, unlocked_at=now
    )
    achievement_repo.create_user_achievement(db, user_achievement)

    unlocked_achievements = [
        UnlockedAchievementInfo(
            code=achievement_def.code,
            name=achievement_def.name,
            description=achievement_def.description,
            reward_title_code=achievement_def.reward_title_code,
        )
    ]
    unlocked_titles: list[UnlockedTitleInfo] = []

    if achievement_def.reward_title_code:
        title_info = _grant_title_by_code(
            db, user_id, achievement_def.reward_title_code, now
        )
        if title_info is not None:
            unlocked_titles.append(title_info)

    return AchievementUnlockResult(
        unlocked_achievements=unlocked_achievements,
        unlocked_titles=unlocked_titles,
    )


def handle_vocabulary_quiz_event(
    db: Session, user_id: UUID, is_correct: bool, mastery_level: int
) -> AchievementUnlockResult:
    all_achievements: list[UnlockedAchievementInfo] = []
    all_titles: list[UnlockedTitleInfo] = []

    if is_correct:
        r = unlock_achievement_by_code(db, user_id, "FIRST_CORRECT_ANSWER")
        all_achievements.extend(r.unlocked_achievements)
        all_titles.extend(r.unlocked_titles)

    if mastery_level >= 1:
        r = unlock_achievement_by_code(db, user_id, "MASTER_ONE_WORD")
        all_achievements.extend(r.unlocked_achievements)
        all_titles.extend(r.unlocked_titles)

    return AchievementUnlockResult(
        unlocked_achievements=all_achievements,
        unlocked_titles=all_titles,
    )


def handle_daily_claim_event(db: Session, user_id: UUID) -> AchievementUnlockResult:
    return unlock_achievement_by_code(db, user_id, "FIRST_DAILY_CLAIM")
