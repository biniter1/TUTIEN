from uuid import UUID

from pydantic import BaseModel


class CultivationProfileResponse(BaseModel):
    id: UUID
    user_id: UUID
    realm: str
    realm_stage: str | None
    cultivation_power: int
    spirit_energy: int
    max_spirit_energy: int
    reputation: int
    streak_days: int

    model_config = {"from_attributes": True}
