from datetime import date
from uuid import UUID

from sqlalchemy import Date, ForeignKey, Text, text
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.dependencies.database import DataModel


class QuestionnaireAnswer(DataModel):
    __tablename__ = "questionnaire_answers"

    id: Mapped[UUID] = mapped_column(
        PostgresUUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    user_id: Mapped[UUID] = mapped_column(
        PostgresUUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False,
    )
    submitted_at: Mapped[date | None] = mapped_column(Date)
    created_at: Mapped[date | None] = mapped_column(Date)
    updated_at: Mapped[date | None] = mapped_column(Date)

    items: Mapped[list["QuestionnaireAnswerItem"]] = relationship(
        "QuestionnaireAnswerItem",
        back_populates="questionnaire_answer",
        cascade="all, delete-orphan",
    )


class QuestionnaireAnswerItem(DataModel):
    __tablename__ = "questionnaire_answer_items"

    id: Mapped[UUID] = mapped_column(
        PostgresUUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    questionnaire_answer_id: Mapped[UUID] = mapped_column(
        PostgresUUID(as_uuid=True),
        ForeignKey("questionnaire_answers.id", ondelete="CASCADE"),
        nullable=False,
    )
    question_id: Mapped[UUID] = mapped_column(
        PostgresUUID(as_uuid=True),
        ForeignKey("questions.id"),
        nullable=False,
    )
    value: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[date | None] = mapped_column(Date)
    updated_at: Mapped[date | None] = mapped_column(Date)

    questionnaire_answer: Mapped["QuestionnaireAnswer"] = relationship(
        "QuestionnaireAnswer",
        back_populates="items",
    )
