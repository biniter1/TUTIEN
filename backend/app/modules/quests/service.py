from datetime import date
from uuid import UUID

from sqlalchemy.orm import Session

from app.modules.quests import repository as quest_repo
from app.modules.quests.models import UserDailyMissionProgress
from app.modules.quests.schemas import DailyMissionResponse, DailyMissionsResponse, MissionProgressUpdate


def get_daily_missions(db: Session, user_id: UUID) -> DailyMissionsResponse:
    # Use server local date for MVP.
    # TODO: Replace with configured timezone (e.g. Asia/Ho_Chi_Minh) when timezone support is added.
    today = date.today()

    missions = quest_repo.list_active_missions(db)

    created_any = False
    mission_responses: list[DailyMissionResponse] = []

    for mission in missions:
        progress = quest_repo.find_progress(db, user_id, mission.id, today)
        if progress is None:
            progress = UserDailyMissionProgress(
                user_id=user_id,
                mission_id=mission.id,
                progress_date=today,
            )
            quest_repo.create_progress(db, progress)
            created_any = True

        # Capture values into Pydantic object now — before commit expires ORM attributes
        mission_responses.append(
            DailyMissionResponse(
                code=mission.code,
                name=mission.name,
                description=mission.description,
                mission_type=mission.mission_type,
                target_value=mission.target_value,
                progress_value=progress.progress_value,
                is_completed=progress.is_completed,
                is_claimed=progress.is_claimed,
                reward_cultivation_power=mission.reward_cultivation_power,
                reward_reputation=mission.reward_reputation,
            )
        )

    if created_any:
        db.commit()

    return DailyMissionsResponse(date=today.isoformat(), missions=mission_responses)


def update_daily_progress_for_quiz(
    db: Session,
    user_id: UUID,
    answered_count: int,
    correct_count: int,
    cultivation_power_gained: int,
    spirit_energy_spent: int,
) -> list[MissionProgressUpdate]:
    # Use server local date for MVP.
    # TODO: Replace with configured timezone (e.g. Asia/Ho_Chi_Minh) when timezone support is added.
    today = date.today()
    missions = quest_repo.list_active_missions(db)
    if not missions:
        return []

    increment_map = {
        "answer_questions": answered_count,
        "correct_answers": correct_count,
        "gain_cultivation_power": cultivation_power_gained,
        "spend_spirit_energy": spirit_energy_spent,
    }

    updated: list[MissionProgressUpdate] = []

    for mission in missions:
        increment = increment_map.get(mission.mission_type, 0)
        if increment == 0:
            continue

        progress = quest_repo.find_progress(db, user_id, mission.id, today)
        if progress is None:
            progress = UserDailyMissionProgress(
                user_id=user_id,
                mission_id=mission.id,
                progress_date=today,
            )
            quest_repo.create_progress(db, progress)

        if progress.is_completed:
            continue

        quest_repo.increment_progress(db, progress, increment, mission.target_value)

        updated.append(
            MissionProgressUpdate(
                code=mission.code,
                progress_value=progress.progress_value,
                target_value=mission.target_value,
                is_completed=progress.is_completed,
            )
        )

    return updated
