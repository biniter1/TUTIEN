from pydantic import BaseModel


class MissionProgressUpdate(BaseModel):
    code: str
    progress_value: int
    target_value: int
    is_completed: bool


class DailyMissionResponse(BaseModel):
    code: str
    name: str
    description: str | None
    mission_type: str
    target_value: int
    progress_value: int
    is_completed: bool
    is_claimed: bool
    reward_cultivation_power: int
    reward_reputation: int


class DailyMissionsResponse(BaseModel):
    date: str
    missions: list[DailyMissionResponse]
