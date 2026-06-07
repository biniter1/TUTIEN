from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user, get_db
from app.modules.achievements import service as achievement_service
from app.modules.achievements.schemas import AchievementsResponse, EquipTitleResponse, TitlesResponse
from app.modules.users.models import User

achievements_router = APIRouter(prefix="/achievements", tags=["achievements"])
titles_router = APIRouter(prefix="/titles", tags=["titles"])


@achievements_router.get("/me", response_model=AchievementsResponse)
def get_my_achievements(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return achievement_service.get_user_achievements(db, current_user.id)


@titles_router.get("/me", response_model=TitlesResponse)
def get_my_titles(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return achievement_service.get_user_titles(db, current_user.id)


@titles_router.post("/{title_code}/equip", response_model=EquipTitleResponse)
def equip_title(
    title_code: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return achievement_service.equip_title(db, current_user.id, title_code)
