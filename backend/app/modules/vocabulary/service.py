from datetime import datetime, timezone
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.modules.cultivation import service as cultivation_service
from app.modules.vocabulary import repository as vocab_repo
from app.modules.vocabulary.models import UserWordProgress, VocabularySet, VocabularyWord
from app.modules.vocabulary.schemas import (
    QuizSubmitRequest,
    QuizSubmitResponse,
    WordProgressResponse,
)

CULTIVATION_POWER_PER_CORRECT = 5
MAX_MASTERY_LEVEL = 5


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


def submit_quiz(db: Session, user_id: UUID, request: QuizSubmitRequest) -> QuizSubmitResponse:
    # 1. Fetch the word
    word = vocab_repo.find_word_by_id(db, request.word_id)
    if word is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Word not found")

    # 2. Determine expected answer based on quiz type
    expected = word.vietnamese if request.quiz_type == "en_to_vi" else word.english

    # 3. Normalize and compare
    normalized_answer = request.answer.strip().lower()
    normalized_expected = expected.strip().lower()

    if request.quiz_type == "en_to_vi":
        # Substring match: "linh hồn" should pass for "linh hồn / tinh thần"
        is_correct = normalized_answer in normalized_expected
    else:
        is_correct = normalized_answer == normalized_expected

    # 4. Get or create progress record for this user+word pair
    progress = vocab_repo.find_progress(db, user_id, request.word_id)
    if progress is None:
        progress = UserWordProgress(user_id=user_id, word_id=request.word_id)
        vocab_repo.create_progress(db, progress)

    # 5. Update progress counters
    if is_correct:
        progress.correct_count += 1
    else:
        progress.wrong_count += 1
    progress.mastery_level = min(MAX_MASTERY_LEVEL, progress.correct_count // 3)
    progress.last_answered_at = datetime.now(timezone.utc)

    # 6. Award cultivation power if correct (cross-module call — no direct DB write here)
    power_gained = 0
    new_power = 0
    if is_correct:
        power_gained = CULTIVATION_POWER_PER_CORRECT
        new_power = cultivation_service.add_cultivation_power(db, user_id, power_gained)
    else:
        profile = cultivation_service.get_profile_by_user_id(db, user_id)
        new_power = profile.cultivation_power if profile else 0

    # 7. Capture progress values before commit (SQLAlchemy expires attributes on commit)
    result_correct_count = progress.correct_count
    result_wrong_count = progress.wrong_count
    result_mastery = progress.mastery_level

    # 8. Single commit — persists UserWordProgress + CultivationProfile atomically
    db.commit()

    return QuizSubmitResponse(
        correct=is_correct,
        expected_answer=expected,
        cultivation_power_gained=power_gained,
        new_cultivation_power=new_power,
        progress=WordProgressResponse(
            correct_count=result_correct_count,
            wrong_count=result_wrong_count,
            mastery_level=result_mastery,
        ),
    )
