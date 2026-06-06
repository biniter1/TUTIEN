from datetime import date
from uuid import UUID

from sqlalchemy.orm import Session

from app.modules.quests.models import DailyMissionDefinition, UserDailyMissionProgress


def list_active_missions(db: Session) -> list[DailyMissionDefinition]:
    return (
        db.query(DailyMissionDefinition)
        .filter(DailyMissionDefinition.is_active.is_(True))
        .all()
    )


def find_progress(
    db: Session,
    user_id: UUID,
    mission_id: UUID,
    progress_date: date,
) -> UserDailyMissionProgress | None:
    return (
        db.query(UserDailyMissionProgress)
        .filter(
            UserDailyMissionProgress.user_id == user_id,
            UserDailyMissionProgress.mission_id == mission_id,
            UserDailyMissionProgress.progress_date == progress_date,
        )
        .first()
    )


def create_progress(
    db: Session, progress: UserDailyMissionProgress
) -> UserDailyMissionProgress:
    db.add(progress)
    db.flush()
    return progress
