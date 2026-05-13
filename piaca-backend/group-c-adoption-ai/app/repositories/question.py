from datetime import date
from uuid import UUID

from fastapi import Depends
from sqlalchemy import func
from sqlalchemy import update as sql_update
from sqlalchemy.orm import Session

from app.dependencies.database import piaca_db
from app.models.questions import Question


class QuestionRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_question(
        self,
        text: str,
        possible_answers: str | None,
        type: str,
        code: int,
        created_at: date,
        updated_at: date,
    ) -> Question:
        return piaca_db.add(
            self.session,
            Question(
                text=text,
                possible_answers=possible_answers,
                type=type,
                code=code,
                created_at=created_at,
                updated_at=updated_at,
            ),
        )

    def get_by_id(self, question_id: UUID) -> Question | None:
        return piaca_db.get_by_id(self.session, Question, question_id)

    def get_all_ordered_by_code(self) -> list[Question]:
        return self.session.query(Question).order_by(Question.code.asc()).all()

    def delete(self, question_id: UUID) -> bool:
        return piaca_db.delete_by_id(self.session, Question, question_id)

    def update_fields(self, question_id: UUID, fields: dict) -> Question | None:
        return piaca_db.update_by_id(self.session, Question, question_id, fields)

    def get_max_code(self) -> int:
        return self.session.query(func.max(Question.code)).scalar() or 0

    def shift_codes_down(self, exclude_id: UUID, old_code: int, new_code: int) -> None:
        self.session.execute(
            sql_update(Question)
            .where(Question.id != exclude_id)
            .where(Question.code > old_code)
            .where(Question.code <= new_code)
            .values(code=Question.code - 1)
        )
        self.session.flush()

    def shift_codes_up(self, exclude_id: UUID, old_code: int, new_code: int) -> None:
        self.session.execute(
            sql_update(Question)
            .where(Question.id != exclude_id)
            .where(Question.code >= new_code)
            .where(Question.code < old_code)
            .values(code=Question.code + 1)
        )
        self.session.flush()


def get_question_repo(
    session: Session = Depends(piaca_db.get_session),
) -> QuestionRepository:
    return QuestionRepository(session=session)
