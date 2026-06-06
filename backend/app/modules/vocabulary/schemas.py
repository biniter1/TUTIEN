from typing import Literal
from uuid import UUID

from pydantic import BaseModel


class VocabularySetResponse(BaseModel):
    id: UUID
    code: str
    name: str
    description: str | None
    theme: str | None
    difficulty: str
    required_realm: str | None
    total_words: int
    is_active: bool

    model_config = {"from_attributes": True}


class VocabularyWordResponse(BaseModel):
    id: UUID
    set_id: UUID
    english: str
    vietnamese: str
    pronunciation: str | None
    example_sentence: str | None
    example_translation: str | None
    difficulty: str

    model_config = {"from_attributes": True}


class QuizSubmitRequest(BaseModel):
    word_id: UUID
    quiz_type: Literal["en_to_vi", "vi_to_en"]
    answer: str


class WordProgressResponse(BaseModel):
    correct_count: int
    wrong_count: int
    mastery_level: int


class QuizSubmitResponse(BaseModel):
    correct: bool
    expected_answer: str
    cultivation_power_gained: int
    new_cultivation_power: int
    spirit_energy_spent: int
    remaining_spirit_energy: int
    progress: WordProgressResponse


class VocabularyProgressSummary(BaseModel):
    total_words_attempted: int
    total_correct: int
    total_wrong: int
    mastered_words: int
    average_mastery_level: float


class WordProgressDetail(BaseModel):
    word_id: UUID
    english: str
    vietnamese: str
    correct_count: int
    wrong_count: int
    mastery_level: int


class SetProgressResponse(BaseModel):
    set_id: UUID
    total_words: int
    attempted_words: int
    mastered_words: int
    completion_percent: float
    words: list[WordProgressDetail]
