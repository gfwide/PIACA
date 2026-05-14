from datetime import date
from uuid import UUID

from fastapi import Depends
from sqlalchemy.orm import Session

from app.dependencies.database import piaca_db
from app.models.report import Report


class ReportRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_report_by_adopter_id(self, adopter_id: UUID) -> Report | None:
        return (
            self.session.query(Report)
            .filter(Report.adopter_id == adopter_id)
            .order_by(Report.updated_at.desc())
            .first()
        )

    def save_report(self, adopter_id: UUID, report_text: str) -> Report:
        today = date.today()
        return piaca_db.add(
            self.session,
            Report(
                report=report_text,
                adopter_id=adopter_id,
                created_at=today,
                updated_at=today,
            ),
        )

    def get_adopter_by_user_id(self, user_id: UUID) -> dict | None:
        raise NotImplementedError

    def get_pet_by_id(self, pet_id: UUID) -> dict | None:
        raise NotImplementedError

    def get_available_pets(self) -> list[dict]:
        raise NotImplementedError


def get_report_repo(
    session: Session = Depends(piaca_db.get_session),
) -> ReportRepository:
    return ReportRepository(session=session)
