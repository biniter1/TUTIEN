from datetime import datetime

from pydantic import BaseModel, Field


class UnlockedAchievementInfo(BaseModel):
    code: str
    name: str
    description: str | None
    reward_title_code: str | None


class UnlockedTitleInfo(BaseModel):
    code: str
    name: str
    rarity: str


class AchievementUnlockResult(BaseModel):
    unlocked_achievements: list[UnlockedAchievementInfo] = Field(default_factory=list)
    unlocked_titles: list[UnlockedTitleInfo] = Field(default_factory=list)


class AchievementResponse(BaseModel):
    code: str
    name: str
    description: str | None
    category: str | None
    is_hidden: bool
    is_unlocked: bool
    unlocked_at: datetime | None
    reward_title_code: str | None


class AchievementsResponse(BaseModel):
    achievements: list[AchievementResponse]


class TitleResponse(BaseModel):
    code: str
    name: str
    description: str | None
    rarity: str
    is_unlocked: bool
    is_equipped: bool
    unlocked_at: datetime | None


class TitlesResponse(BaseModel):
    titles: list[TitleResponse]
