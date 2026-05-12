from datetime import date
from uuid import UUID

from fastapi import Depends

from app.models.survey import QuestionnaireAnswer
from app.repositories.survey import SurveyRepository, get_survey_repo
from app.schemas.survey import (
    AnswerItemResponse,
    SubmitSurveyRequest,
    SurveyAnswerResponse,
)


class SurveyService:
    def __init__(self, repo: SurveyRepository):
        self.repo = repo

    def submit_survey(
        self, user_id: UUID, data: SubmitSurveyRequest
    ) -> SurveyAnswerResponse:
        today = date.today()
        answer = self.repo.create_answer(user_id, today)
        items = [
            self.repo.create_answer_item(
                answer.id, item_data.question_id, item_data.value, today
            )
            for item_data in data.answers
        ]
        return self._to_response(answer, items)

    def get_user_answers(self, user_id: UUID) -> SurveyAnswerResponse | None:
        answer = self.repo.get_latest_answer_by_user(user_id)
        if answer is None:
            return None
        return self._to_response(answer, answer.items)

    def update_answers(
        self, user_id: UUID, data: SubmitSurveyRequest
    ) -> SurveyAnswerResponse | None:
        answer = self.repo.get_latest_answer_by_user(user_id)
        if answer is None:
            return None

        self.repo.delete_answer_items(answer)
        today = date.today()
        items = [
            self.repo.create_answer_item(
                answer.id, item_data.question_id, item_data.value, today
            )
            for item_data in data.answers
        ]
        self.repo.update_answer_timestamp(answer, today)
        return self._to_response(answer, items)

    def _to_response(self, answer: QuestionnaireAnswer, items) -> SurveyAnswerResponse:
        return SurveyAnswerResponse(
            id=answer.id,
            user_id=answer.user_id,
            submitted_at=answer.submitted_at,
            answers=[
                AnswerItemResponse(
                    id=item.id, question_id=item.question_id, value=item.value
                )
                for item in items
            ],
        )


def get_survey_service(
    repo: SurveyRepository = Depends(get_survey_repo),
) -> SurveyService:
    return SurveyService(repo=repo)
