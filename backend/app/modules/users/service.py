from uuid import UUID

from sqlalchemy.orm import Session

from app.modules.users import repository as user_repo
from app.modules.users.models import User


def get_user_by_id(db: Session, user_id: UUID) -> User | None:
    return user_repo.find_by_id(db, user_id)
