from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user, get_db
from app.modules.cultivation import service as cultivation_service
from app.modules.cultivation.schemas import CultivationProfileResponse
from app.modules.users.models import User

router = APIRouter(prefix="/cultivation", tags=["cultivation"])


@router.get("/me", response_model=CultivationProfileResponse)
def get_my_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    profile = cultivation_service.get_profile_by_user_id(db, current_user.id)
    if profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cultivation profile not found",
        )
    return profile
