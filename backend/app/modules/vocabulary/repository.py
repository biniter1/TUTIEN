from uuid import UUID

from sqlalchemy.orm import Session

from app.modules.vocabulary.models import UserWordProgress, VocabularySet, VocabularyWord


def list_active_sets(db: Session) -> list[VocabularySet]:
    return db.query(VocabularySet).filter(VocabularySet.is_active.is_(True)).all()


def find_set_by_id(db: Session, set_id: UUID) -> VocabularySet | None:
    return db.query(VocabularySet).filter(VocabularySet.id == set_id).first()


def list_words_by_set_id(db: Session, set_id: UUID) -> list[VocabularyWord]:
    return db.query(VocabularyWord).filter(VocabularyWord.set_id == set_id).all()


def find_word_by_id(db: Session, word_id: UUID) -> VocabularyWord | None:
    return db.query(VocabularyWord).filter(VocabularyWord.id == word_id).first()


def find_progress(db: Session, user_id: UUID, word_id: UUID) -> UserWordProgress | None:
    return (
        db.query(UserWordProgress)
        .filter(UserWordProgress.user_id == user_id, UserWordProgress.word_id == word_id)
        .first()
    )


def create_progress(db: Session, progress: UserWordProgress) -> UserWordProgress:
    db.add(progress)
    db.flush()
    return progress


def get_user_progress_all(db: Session, user_id: UUID) -> list[UserWordProgress]:
    return db.query(UserWordProgress).filter(UserWordProgress.user_id == user_id).all()


def get_user_progress_for_set(
    db: Session, user_id: UUID, word_ids: list[UUID]
) -> list[UserWordProgress]:
    if not word_ids:
        return []
    return (
        db.query(UserWordProgress)
        .filter(
            UserWordProgress.user_id == user_id,
            UserWordProgress.word_id.in_(word_ids),
        )
        .all()
    )
