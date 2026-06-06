from uuid import UUID

from sqlalchemy.orm import Session

from app.modules.vocabulary.models import VocabularySet, VocabularyWord


def list_active_sets(db: Session) -> list[VocabularySet]:
    return db.query(VocabularySet).filter(VocabularySet.is_active.is_(True)).all()


def find_set_by_id(db: Session, set_id: UUID) -> VocabularySet | None:
    return db.query(VocabularySet).filter(VocabularySet.id == set_id).first()


def list_words_by_set_id(db: Session, set_id: UUID) -> list[VocabularyWord]:
    return db.query(VocabularyWord).filter(VocabularyWord.set_id == set_id).all()
