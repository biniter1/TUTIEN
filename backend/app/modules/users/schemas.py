from uuid import UUID

from pydantic import BaseModel


class UserResponse(BaseModel):
    id: UUID
    email: str
    username: str
    dao_name: str | None
    faction: str | None
    is_active: bool

    model_config = {"from_attributes": True}
