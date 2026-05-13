import json
from datetime import date, datetime, time
from uuid import UUID

from fastapi import Depends

from app.models.questions import Question
from app.repositories.question import QuestionRepository, get_question_repo
from app.schemas.questions import (
    CreateQuestionRequest,
    QuestionResponse,
    QuestionTypes,
    SelectableOption,
    UpdateQuestionRequest,
)
from app.schemas.shared.responses import (
    CreatedResponse,
    DeletedResponse,
    UpdatedResponse,
)


class QuestionService:
    def __init__(self, repo: QuestionRepository):
        self.repo = repo

    def create_question(self, data: CreateQuestionRequest) -> CreatedResponse:
        possible_answers = (
            json.dumps([opt.model_dump() for opt in data.possible_answers])
            if data.possible_answers
            else None
        )
        code = self.repo.get_max_code() + 1
        question = self.repo.create_question(
            text=data.question,
            possible_answers=possible_answers,
            type=data.type.value,
            code=code,
            created_at=data.created_at,
            updated_at=data.updated_at,
        )
        return CreatedResponse(
            id=question.id,
            created_at=self._to_datetime(question.created_at),
            function_response=self._to_schema(question).model_dump(),
        )

    def get_question(self, question_id: UUID) -> QuestionResponse | None:
        question = self.repo.get_by_id(question_id)
        if question is None:
            return None
        return self._to_schema(question)

    def get_all_questions(self) -> list[QuestionResponse]:
        return [self._to_schema(q) for q in self.repo.get_all_ordered_by_code()]

    def delete_question(self, question_id: UUID) -> DeletedResponse:
        deleted = self.repo.delete(question_id)
        return DeletedResponse(id=question_id, deleted=deleted)

    def update_question(
        self, question_id: UUID, data: UpdateQuestionRequest
    ) -> UpdatedResponse | None:
        fields: dict = {"updated_at": date.today()}

        if data.question is not None:
            fields["text"] = data.question
        if data.type is not None:
            fields["type"] = data.type.value
        if data.possible_answers is not None:
            fields["possible_answers"] = (
                json.dumps([opt.model_dump() for opt in data.possible_answers])
                if data.possible_answers
                else None
            )

        question = self.repo.update_fields(question_id, fields)
        if question is None:
            return None

        return UpdatedResponse(
            id=question.id,
            updated_at=self._to_datetime(question.updated_at),
            function_response=self._to_schema(question).model_dump(),
        )

    def reorder_question(
        self, question_id: UUID, new_code: int
    ) -> UpdatedResponse | None:
        question = self.repo.get_by_id(question_id)
        if question is None:
            return None

        old_code = question.code
        if old_code is None:
            raise ValueError("Question has no code assigned and cannot be reordered")

        new_code = max(1, min(new_code, self.repo.get_max_code()))

        if old_code != new_code:
            if new_code > old_code:
                self.repo.shift_codes_down(question_id, old_code, new_code)
            else:
                self.repo.shift_codes_up(question_id, old_code, new_code)

        question = self.repo.update_fields(
            question_id, {"code": new_code, "updated_at": date.today()}
        )
        if question is None:
            return None

        return UpdatedResponse(
            id=question.id,
            updated_at=self._to_datetime(question.updated_at),
            function_response=self._to_schema(question).model_dump(),
        )

    def _to_schema(self, question: Question) -> QuestionResponse:
        possible_answers = (
            [SelectableOption(**opt) for opt in json.loads(question.possible_answers)]
            if question.possible_answers
            else []
        )
        return QuestionResponse(
            id=question.id,
            code=question.code,
            type=QuestionTypes(question.type),
            question=question.text,
            possible_answers=possible_answers,
            created_at=question.created_at,
            updated_at=question.updated_at,
        )

    def _to_datetime(self, value: date | None) -> datetime:
        if value is None:
            return datetime.now()
        return datetime.combine(value, time())


def get_question_service(
    repo: QuestionRepository = Depends(get_question_repo),
) -> QuestionService:
    return QuestionService(repo=repo)
