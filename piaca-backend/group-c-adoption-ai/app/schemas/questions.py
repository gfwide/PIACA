from datetime import date
from uuid import UUID
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, model_validator


class QuestionTypes(Enum):
    TEXT = "text"
    BOOLEAN = "boolean"
    SELECT = "select"
    CHECKBOX = "checkbox"


class SelectableOption(BaseModel):
    option: str


class Question(BaseModel):
    type: QuestionTypes = Field(default=QuestionTypes.TEXT)
    question: str
    possible_answers: list[SelectableOption] = Field(default=[])

    @model_validator(mode="after")
    def validate_possible_answers(self) -> "Question":
        if self.type in (QuestionTypes.SELECT, QuestionTypes.CHECKBOX):
            if len(self.possible_answers) < 2:
                raise ValueError(
                    "possible_answers must have at least 2 options for select and checkbox types"
                )
        return self


class CreateQuestionRequest(Question):
    created_at: date = Field(default_factory=date.today)
    updated_at: date = Field(default_factory=date.today)


class UpdateQuestionRequest(BaseModel):
    question: Optional[str] = None
    type: Optional[QuestionTypes] = None
    possible_answers: Optional[list[SelectableOption]] = None

    @model_validator(mode="after")
    def validate_possible_answers(self) -> "UpdateQuestionRequest":
        if self.type in (QuestionTypes.SELECT, QuestionTypes.CHECKBOX):
            if self.possible_answers is not None and len(self.possible_answers) < 2:
                raise ValueError(
                    "possible_answers must have at least 2 options for select and checkbox types"
                )
        return self


class QuestionResponse(BaseModel):
    id: UUID
    code: Optional[int] = None
    type: QuestionTypes
    question: str
    possible_answers: list[SelectableOption] = Field(default=[])
    created_at: Optional[date] = None
    updated_at: Optional[date] = None
