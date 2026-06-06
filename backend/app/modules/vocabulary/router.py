from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user, get_db
from app.modules.users.models import User
from app.modules.vocabulary import service as vocab_service
from app.modules.vocabulary.schemas import (
    QuizSubmitRequest,
    QuizSubmitResponse,
    SetProgressResponse,
    VocabularyProgressSummary,
    VocabularySetResponse,
    VocabularyWordResponse,
)

router = APIRouter(prefix="/vocabulary", tags=["vocabulary"])

# Specific static routes first — must come before any dynamic /{param} routes
# that could otherwise shadow them.

@router.get("/sets", response_model=list[VocabularySetResponse])
def list_sets(db: Session = Depends(get_db)):
    return vocab_service.list_sets(db)


@router.get("/progress/me", response_model=VocabularyProgressSummary)
def get_progress_summary(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return vocab_service.get_progress_summary(db, current_user.id)


@router.post("/quiz/submit", response_model=QuizSubmitResponse)
def submit_quiz(
    request: QuizSubmitRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return vocab_service.submit_quiz(db, current_user.id, request)


# Dynamic routes after all static routes

@router.get("/sets/{set_id}", response_model=VocabularySetResponse)
def get_set(set_id: UUID, db: Session = Depends(get_db)):
    return vocab_service.get_set(db, set_id)


@router.get("/sets/{set_id}/words", response_model=list[VocabularyWordResponse])
def get_words(set_id: UUID, db: Session = Depends(get_db)):
    return vocab_service.get_words(db, set_id)


@router.get("/sets/{set_id}/progress", response_model=SetProgressResponse)
def get_set_progress(
    set_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return vocab_service.get_set_progress(db, current_user.id, set_id)
