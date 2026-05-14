from datetime import date
from uuid import UUID, uuid4

from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column

from app.dependencies.database import DataModel


class Report(DataModel):
    __tablename__ = "reports"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    report: Mapped[str] = mapped_column(Text)
    adopter_id: Mapped[UUID]
    created_at: Mapped[date]
    updated_at: Mapped[date]
