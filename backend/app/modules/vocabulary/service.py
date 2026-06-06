from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.modules.vocabulary import repository as vocab_repo
from app.modules.vocabulary.models import VocabularySet, VocabularyWord


def list_sets(db: Session) -> list[VocabularySet]:
    return vocab_repo.list_active_sets(db)


def get_set(db: Session, set_id: UUID) -> VocabularySet:
    vocab_set = vocab_repo.find_set_by_id(db, set_id)
    if vocab_set is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vocabulary set not found",
        )
    return vocab_set


def get_words(db: Session, set_id: UUID) -> list[VocabularyWord]:
    get_set(db, set_id)  # validates set exists, raises 404 if not
    return vocab_repo.list_words_by_set_id(db, set_id)
