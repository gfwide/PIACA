from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from app.api.routers.doc_examples.survey_question import (
    CREATE_QUESTION_EXAMPLES,
    REORDER_QUESTION_EXAMPLES,
    UPDATE_QUESTION_EXAMPLES,
)
from app.schemas.questions import (
    CreateQuestionRequest,
    QuestionResponse,
    UpdateQuestionRequest,
)
from app.schemas.shared.responses import (
    CreatedResponse,
    DeletedResponse,
    UpdatedResponse,
)
from app.services.question import QuestionService, get_question_service

router = APIRouter(prefix="/questions")


@router.post("/", response_model=CreatedResponse, status_code=201)
def create_question(
    data: Annotated[CreateQuestionRequest, CREATE_QUESTION_EXAMPLES],
    question_service: QuestionService = Depends(get_question_service),
):
    return question_service.create_question(data)


@router.delete("/{question_id}", response_model=DeletedResponse)
def delete_question(
    question_id: UUID,
    question_service: QuestionService = Depends(get_question_service),
):
    return question_service.delete_question(question_id)


@router.patch("/{question_id}/reorder", response_model=UpdatedResponse)
def reorder_question(
    question_id: UUID,
    new_code: int = REORDER_QUESTION_EXAMPLES,
    question_service: QuestionService = Depends(get_question_service),
):
    try:
        result = question_service.reorder_question(question_id, new_code)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    if result is None:
        raise HTTPException(status_code=404, detail="Question not found")
    return result


@router.patch("/{question_id}", response_model=UpdatedResponse)
def update_question(
    question_id: UUID,
    data: Annotated[UpdateQuestionRequest, UPDATE_QUESTION_EXAMPLES],
    question_service: QuestionService = Depends(get_question_service),
):
    question = question_service.update_question(question_id, data)
    if question is None:
        raise HTTPException(status_code=404, detail="Question not found")

    return question


@router.get("/all", response_model=list[QuestionResponse])
def get_all_questions(
    question_service: QuestionService = Depends(get_question_service),
):
    return question_service.get_all_questions()


@router.get("/{question_id}", response_model=QuestionResponse)
def get_one_question(
    question_id: UUID,
    question_service: QuestionService = Depends(get_question_service),
):
    question = question_service.get_question(question_id)
    if question is None:
        raise HTTPException(status_code=404, detail="Question not found")

    return question
