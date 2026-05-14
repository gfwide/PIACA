from uuid import UUID

from fastapi import Depends, HTTPException

from app.dependencies.gemini_client import gemini_client
from app.repositories.report import ReportRepository, get_report_repo
from app.schemas.report import ReportOut, SinglePetReport
from app.schemas.survey import SurveyAnswerEnrichedResponse
from app.services.survey import SurveyService, get_survey_service


class ReportService:
    def __init__(self, repo: ReportRepository, survey_service: SurveyService):
        self.repo = repo
        self.survey_service = survey_service

    async def generate_single_pet_report(self, user_id: UUID, pet_id: UUID) -> SinglePetReport:
        adopter = self.repo.get_adopter_by_user_id(user_id)
        if adopter is None:
            raise HTTPException(status_code=404, detail="Adopter not found")

        pet = self.repo.get_pet_by_id(pet_id)
        if pet is None:
            raise HTTPException(status_code=404, detail="Pet not found")

        survey = self.survey_service.get_user_answers(user_id)
        prompt = self._build_single_pet_prompt(adopter, survey, pet)
        report_text = await gemini_client.complete(prompt)
        return SinglePetReport(report=report_text)

    async def get_or_generate_general_report(self, user_id: UUID) -> ReportOut:
        adopter = self.repo.get_adopter_by_user_id(user_id)
        if adopter is None:
            raise HTTPException(status_code=404, detail="Adopter not found")

        existing = self.repo.get_report_by_adopter_id(adopter["id"])
        if existing:
            return ReportOut.model_validate(existing)

        survey = self.survey_service.get_user_answers(user_id)
        if survey is None or not survey.answers:
            raise HTTPException(status_code=422, detail="Adopter has no survey answers submitted")

        pets = self.repo.get_available_pets()
        if not pets:
            raise HTTPException(status_code=404, detail="No pets available for adoption")

        prompt = self._build_general_report_prompt(adopter, survey, pets)
        report_text = await gemini_client.complete(prompt)

        saved = self.repo.save_report(adopter["id"], report_text)
        return ReportOut.model_validate(saved)

    def _build_single_pet_prompt(
        self,
        adopter: dict,
        survey: SurveyAnswerEnrichedResponse | None,
        pet: dict,
    ) -> str:
        raise NotImplementedError

    def _build_general_report_prompt(
        self,
        adopter: dict,
        survey: SurveyAnswerEnrichedResponse,
        pets: list[dict],
    ) -> str:
        raise NotImplementedError


def get_report_service(
    repo: ReportRepository = Depends(get_report_repo),
    survey_service: SurveyService = Depends(get_survey_service),
) -> ReportService:
    return ReportService(repo=repo, survey_service=survey_service)
