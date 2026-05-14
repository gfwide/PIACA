from __future__ import annotations

from typing import Literal, Optional
from uuid import UUID
from pydantic import BaseModel, Field


class CreateAdoptionRequest(BaseModel):
    pet_id: UUID
    message: Optional[str] = None


class UpdateAdoptionStatusRequest(BaseModel):
    action: Literal["advance", "reject"]


class Adoption(BaseModel):
    id: str = Field(alias="_id")
    pet_name: str