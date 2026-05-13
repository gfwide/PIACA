from datetime import date
from uuid import UUID

from fastapi import Depends
from sqlalchemy.orm import Session

from app.dependencies.database import piaca_db
from app.models.survey import QuestionnaireAnswer, QuestionnaireAnswerItem


class SurveyRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_answer(self, user_id: UUID, today: date) -> QuestionnaireAnswer:
        return piaca_db.add(
            self.session,
            QuestionnaireAnswer(
                user_id=user_id,
                submitted_at=today,
                created_at=today,
                updated_at=today,
            ),
        )

    def create_answer_item(
        self, answer_id: UUID, question_id: UUID, value: str, today: date
    ) -> QuestionnaireAnswerItem:
        return piaca_db.add(
            self.session,
            QuestionnaireAnswerItem(
                questionnaire_answer_id=answer_id,
                question_id=question_id,
                value=value,
                created_at=today,
                updated_at=today,
            ),
        )

    def get_latest_answer_by_user(self, user_id: UUID) -> QuestionnaireAnswer | None:
        return (
            self.session.query(QuestionnaireAnswer)
            .filter(QuestionnaireAnswer.user_id == user_id)
            .order_by(QuestionnaireAnswer.submitted_at.desc())
            .first()
        )

    def delete_answer_items(self, answer: QuestionnaireAnswer) -> None:
        for item in list(answer.items):
            self.session.delete(item)
        self.session.flush()

    def update_answer_timestamp(self, answer: QuestionnaireAnswer, today: date) -> None:
        answer.updated_at = today
        self.session.flush()
        self.session.refresh(answer)


def get_survey_repo(
    session: Session = Depends(piaca_db.get_session),
) -> SurveyRepository:
    return SurveyRepository(session=session)
