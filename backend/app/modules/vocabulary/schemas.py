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
