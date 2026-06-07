from datetime import datetime

from pydantic import BaseModel


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
