from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import create_access_token, hash_password, verify_password
from app.modules.auth import repository as auth_repo
from app.modules.auth.schemas import LoginRequest, RegisterRequest
from app.modules.cultivation import service as cultivation_service
from app.modules.users.models import User


def register(db: Session, request: RegisterRequest) -> User:
    if auth_repo.find_by_email(db, request.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    if auth_repo.find_by_username(db, request.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken",
        )
    user = User(
        email=request.email,
        username=request.username,
        password_hash=hash_password(request.password),
        dao_name=request.dao_name,
    )
    auth_repo.create_user(db, user)  # flush only — user.id is now available
    cultivation_service.create_default_profile(db, user.id)  # flush only

    db.commit()      # single commit — both user and profile are persisted atomically
    db.refresh(user)
    return user


def login(db: Session, request: LoginRequest) -> str:
    user = auth_repo.find_by_email(db, request.email)
    if not user or not verify_password(request.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is inactive",
        )
    return create_access_token({"sub": str(user.id)})
