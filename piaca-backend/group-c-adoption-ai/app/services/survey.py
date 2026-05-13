from datetime import date
from uuid import UUID

from fastapi import Depends

from app.models.survey import QuestionnaireAnswer
from app.repositories.survey import SurveyRepository, get_survey_repo
from app.schemas.questions import QuestionTypes
from app.schemas.survey import (
    AnswerItemEnrichedResponse,
    AnswerItemRequest,
    AnswerItemResponse,
    SubmitSurveyRequest,
    SurveyAnswerEnrichedResponse,
    SurveyAnswerResponse,
)
from app.services.question import QuestionService, get_question_service


class MissingAnswersError(Exception):
    def __init__(self, missing: list[UUID]):
        self.missing = missing


class InvalidAnswerValueError(Exception):
    def __init__(self, errors: list[dict]):
        self.errors = errors


class SurveyService:
    def __init__(self, repo: SurveyRepository, question_service: QuestionService):
        self.repo = repo
        self.question_service = question_service

    def submit_survey(
        self, user_id: UUID, data: SubmitSurveyRequest
    ) -> SurveyAnswerResponse:
        missing = self.handle_not_matching_answers_amount(data.answers)
        if missing:
            raise MissingAnswersError(missing)

        invalid = self.validate_answer_values(data.answers)
        if invalid:
            raise InvalidAnswerValueError(invalid)

        today = date.today()
        answer = self.repo.create_answer(user_id, today)
        items = [
            self.repo.create_answer_item(
                answer.id, item_data.question_id, item_data.value, today
            )
            for item_data in data.answers
        ]
        return self._to_response(answer, items)

    def get_user_answers(self, user_id: UUID) -> SurveyAnswerEnrichedResponse | None:
        answer = self.repo.get_latest_answer_by_user(user_id)
        if answer is None:
            return None

        questions_by_id = {
            q.id: q.question for q in self.question_service.get_all_questions()
        }
        return SurveyAnswerEnrichedResponse(
            id=answer.id,
            user_id=answer.user_id,
            submitted_at=answer.submitted_at,
            answers=[
                AnswerItemEnrichedResponse(
                    question=questions_by_id.get(item.question_id, str(item.question_id)),
                    answer=item.value,
                )
                for item in answer.items
            ],
        )

    def update_answers(
        self, user_id: UUID, data: SubmitSurveyRequest
    ) -> SurveyAnswerResponse | None:
        missing = self.handle_not_matching_answers_amount(data.answers)
        if missing:
            raise MissingAnswersError(missing)

        invalid = self.validate_answer_values(data.answers)
        if invalid:
            raise InvalidAnswerValueError(invalid)

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

    def handle_not_matching_answers_amount(
        self, submitted_answers: list[AnswerItemRequest]
    ) -> list[UUID]:
        all_questions = self.question_service.get_all_questions()
        submitted_ids = {a.question_id for a in submitted_answers}
        return [q.id for q in all_questions if q.id not in submitted_ids]

    def validate_answer_values(
        self, submitted_answers: list[AnswerItemRequest]
    ) -> list[dict]:
        all_questions = self.question_service.get_all_questions()
        questions_by_id = {q.id: q for q in all_questions}

        errors = []
        for answer in submitted_answers:
            question = questions_by_id.get(answer.question_id)
            if question is None or not question.possible_answers:
                continue

            valid_options = {opt.option for opt in question.possible_answers}

            if question.type == QuestionTypes.SELECT:
                if answer.value not in valid_options:
                    errors.append({
                        "question_id": str(answer.question_id),
                        "question": question.question,
                        "submitted_value": answer.value,
                        "valid_options": list(valid_options),
                        "error": "Value must be one of the valid options",
                    })

            elif question.type == QuestionTypes.CHECKBOX:
                submitted_values = [v.strip() for v in answer.value.split(",")]
                invalid_values = [v for v in submitted_values if v not in valid_options]
                if invalid_values:
                    errors.append({
                        "question_id": str(answer.question_id),
                        "question": question.question,
                        "invalid_values": invalid_values,
                        "valid_options": list(valid_options),
                        "error": "All comma-separated values must be valid options",
                    })

        return errors

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
    question_service: QuestionService = Depends(get_question_service),
) -> SurveyService:
    return SurveyService(repo=repo, question_service=question_service)
