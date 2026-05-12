from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from app.schemas.survey import SubmitSurveyRequest, SurveyAnswerResponse
from app.services.survey import SurveyService, get_survey_service

router = APIRouter(tags=["survey"])


@router.post("/{user_id}", response_model=SurveyAnswerResponse, status_code=201)
def answer_survey(
    user_id: UUID,
    body: SubmitSurveyRequest,
    survey_service: SurveyService = Depends(get_survey_service),
) -> SurveyAnswerResponse:
    return survey_service.submit_survey(user_id, body)


@router.get("/{user_id}", response_model=SurveyAnswerResponse)
def get_user_answers(
    user_id: UUID,
    survey_service: SurveyService = Depends(get_survey_service),
) -> SurveyAnswerResponse:
    result = survey_service.get_user_answers(user_id)
    if result is None:
        raise HTTPException(
            status_code=404, detail="No survey answers found for this user"
        )
    return result


@router.put("/{user_id}", response_model=SurveyAnswerResponse)
def update_answers(
    user_id: UUID,
    body: SubmitSurveyRequest,
    survey_service: SurveyService = Depends(get_survey_service),
) -> SurveyAnswerResponse:
    result = survey_service.update_answers(user_id, body)
    if result is None:
        raise HTTPException(
            status_code=404, detail="No survey answers found for this user"
        )
    return result
