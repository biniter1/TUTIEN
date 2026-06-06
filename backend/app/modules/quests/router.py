from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user, get_db
from app.modules.quests import service as quest_service
from app.modules.quests.schemas import DailyMissionsResponse
from app.modules.users.models import User

router = APIRouter(prefix="/quests", tags=["quests"])


@router.get("/daily", response_model=DailyMissionsResponse)
def get_daily_missions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return quest_service.get_daily_missions(db, current_user.id)
