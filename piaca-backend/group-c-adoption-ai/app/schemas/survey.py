from datetime import date
from uuid import UUID

from pydantic import BaseModel


class AnswerItemRequest(BaseModel):
    question_id: UUID
    value: str


class SubmitSurveyRequest(BaseModel):
    answers: list[AnswerItemRequest]


class AnswerItemResponse(BaseModel):
    id: UUID
    question_id: UUID
    value: str | None = None


class SurveyAnswerResponse(BaseModel):
    id: UUID
    user_id: UUID
    submitted_at: date | None = None
    answers: list[AnswerItemResponse]
