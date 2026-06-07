from datetime import datetime, timezone
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.modules.cultivation import service as cultivation_service
from app.modules.quests import service as quest_service
from app.modules.vocabulary import repository as vocab_repo
from app.modules.vocabulary.models import UserWordProgress, VocabularySet, VocabularyWord
from app.modules.vocabulary.schemas import (
    QuizMissionProgressUpdate,
    QuizSubmitRequest,
    QuizSubmitResponse,
    SetProgressResponse,
    VocabularyProgressSummary,
    WordProgressDetail,
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


def get_progress_summary(db: Session, user_id: UUID) -> VocabularyProgressSummary:
    records = vocab_repo.get_user_progress_all(db, user_id)
    if not records:
        return VocabularyProgressSummary(
            total_words_attempted=0,
            total_correct=0,
            total_wrong=0,
            mastered_words=0,
            average_mastery_level=0.0,
        )
    total_correct = sum(r.correct_count for r in records)
    total_wrong = sum(r.wrong_count for r in records)
    mastered_words = sum(1 for r in records if r.mastery_level >= 5)
    average_mastery = round(sum(r.mastery_level for r in records) / len(records), 2)
    return VocabularyProgressSummary(
        total_words_attempted=len(records),
        total_correct=total_correct,
        total_wrong=total_wrong,
        mastered_words=mastered_words,
        average_mastery_level=average_mastery,
    )


def get_set_progress(db: Session, user_id: UUID, set_id: UUID) -> SetProgressResponse:
    get_set(db, set_id)  # raises 404 if set not found
    words = vocab_repo.list_words_by_set_id(db, set_id)

    total_words = len(words)
    word_ids = [w.id for w in words]
    word_lookup = {w.id: w for w in words}

    progress_records = vocab_repo.get_user_progress_for_set(db, user_id, word_ids)

    attempted_words = len(progress_records)
    mastered_words = sum(1 for p in progress_records if p.mastery_level >= 5)
    completion_percent = round(attempted_words / total_words * 100, 1) if total_words > 0 else 0.0

    word_details = [
        WordProgressDetail(
            word_id=p.word_id,
            english=word_lookup[p.word_id].english,
            vietnamese=word_lookup[p.word_id].vietnamese,
            correct_count=p.correct_count,
            wrong_count=p.wrong_count,
            mastery_level=p.mastery_level,
        )
        for p in progress_records
        if p.word_id in word_lookup
    ]

    return SetProgressResponse(
        set_id=set_id,
        total_words=total_words,
        attempted_words=attempted_words,
        mastered_words=mastered_words,
        completion_percent=completion_percent,
        words=word_details,
    )


SPIRIT_ENERGY_PER_QUIZ = 1


def submit_quiz(db: Session, user_id: UUID, request: QuizSubmitRequest) -> QuizSubmitResponse:
    # 1. Validate word — pure read, no mutation yet; invalid word_id never costs energy
    word = vocab_repo.find_word_by_id(db, request.word_id)
    if word is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Word not found")

    # 2. Evaluate answer — pure logic, no DB write
    expected = word.vietnamese if request.quiz_type == "en_to_vi" else word.english
    normalized_answer = request.answer.strip().lower()
    normalized_expected = expected.strip().lower()
    # Substring match handles Vietnamese values like "linh hồn / tinh thần"
    is_correct = (
        normalized_answer in normalized_expected
        if request.quiz_type == "en_to_vi"
        else normalized_answer == normalized_expected
    )

    # 3. Mutation block — rollback on any unexpected error to avoid partial state
    power_gained = 0
    new_power = 0
    remaining_energy = 0
    result_correct_count = 0
    result_wrong_count = 0
    result_mastery = 0

    try:
        # 3a. Deduct spirit energy — raises 400 before mutating if balance is insufficient,
        #     raises 404 if cultivation profile is missing.
        remaining_energy = cultivation_service.spend_spirit_energy(
            db, user_id, SPIRIT_ENERGY_PER_QUIZ
        )

        # 3b. Get or create progress record
        progress = vocab_repo.find_progress(db, user_id, request.word_id)
        if progress is None:
            progress = UserWordProgress(user_id=user_id, word_id=request.word_id)
            vocab_repo.create_progress(db, progress)

        # 3c. Update progress counters
        if is_correct:
            progress.correct_count += 1
        else:
            progress.wrong_count += 1
        progress.mastery_level = min(MAX_MASTERY_LEVEL, progress.correct_count // 3)
        progress.last_answered_at = datetime.now(timezone.utc)

        # 3d. Award cultivation power on correct answer
        if is_correct:
            power_gained = CULTIVATION_POWER_PER_CORRECT
            new_power = cultivation_service.add_cultivation_power(db, user_id, power_gained)
        else:
            profile = cultivation_service.get_profile_by_user_id(db, user_id)
            new_power = profile.cultivation_power if profile else 0

        # 3e. Update daily mission progress — no commit; stays in this transaction
        mission_updates = quest_service.update_daily_progress_for_quiz(
            db,
            user_id=user_id,
            answered_count=1,
            correct_count=1 if is_correct else 0,
            cultivation_power_gained=power_gained,
            spirit_energy_spent=SPIRIT_ENERGY_PER_QUIZ,
        )
        # Convert to vocabulary response schema (Pydantic objects — safe after commit)
        daily_missions_updated = [
            QuizMissionProgressUpdate(
                code=m.code,
                progress_value=m.progress_value,
                target_value=m.target_value,
                is_completed=m.is_completed,
            )
            for m in mission_updates
        ]

        # 3f. Capture ORM attribute values before commit (attributes expire after commit)
        result_correct_count = progress.correct_count
        result_wrong_count = progress.wrong_count
        result_mastery = progress.mastery_level

        # 3g. Single commit — word progress + spirit_energy + cultivation_power + quest progress atomic
        db.commit()

    except Exception:
        db.rollback()
        raise

    return QuizSubmitResponse(
        correct=is_correct,
        expected_answer=expected,
        cultivation_power_gained=power_gained,
        new_cultivation_power=new_power,
        spirit_energy_spent=SPIRIT_ENERGY_PER_QUIZ,
        remaining_spirit_energy=remaining_energy,
        progress=WordProgressResponse(
            correct_count=result_correct_count,
            wrong_count=result_wrong_count,
            mastery_level=result_mastery,
        ),
        daily_missions_updated=daily_missions_updated,
    )
