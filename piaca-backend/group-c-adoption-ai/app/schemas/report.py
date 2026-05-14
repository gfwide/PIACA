from datetime import date
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ReportOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    report: str
    adopter_id: UUID
    created_at: date
    updated_at: date


class SinglePetReport(BaseModel):
    report: str
