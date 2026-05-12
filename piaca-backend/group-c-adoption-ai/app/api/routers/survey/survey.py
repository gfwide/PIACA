from uuid import UUID

from app.schemas.survey import SubmitSurveyRequest, SurveyAnswerResponse
from app.services.survey import (
    InvalidAnswerValueError,
    MissingAnswersError,
    SurveyService,
    get_survey_service,
)
from fastapi import APIRouter, Depends, HTTPException

router = APIRouter(tags=["survey"])


@router.post("/{user_id}", response_model=SurveyAnswerResponse, status_code=201)
def answer_survey(
    user_id: UUID,
    body: SubmitSurveyRequest,
    survey_service: SurveyService = Depends(get_survey_service),
) -> SurveyAnswerResponse:
    try:
        return survey_service.submit_survey(user_id, body)
    except MissingAnswersError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "message": "Not all questions were answered",
                "missing_questions": [str(q) for q in e.missing],
            },
        )
    except InvalidAnswerValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "message": "Some answers contain invalid values",
                "errors": e.errors,
            },
        )


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
    try:
        result = survey_service.update_answers(user_id, body)
    except MissingAnswersError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "message": "Not all questions were answered",
                "missing_questions": [str(q) for q in e.missing],
            },
        )
    except InvalidAnswerValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "message": "Some answers contain invalid values",
                "errors": e.errors,
            },
        )
    if result is None:
        raise HTTPException(
            status_code=404, detail="No survey answers found for this user"
        )
    return result
