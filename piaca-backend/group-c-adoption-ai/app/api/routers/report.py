from uuid import UUID

from fastapi import APIRouter, Depends

from app.schemas.report import ReportOut, SinglePetReport
from app.services.report import ReportService, get_report_service

router = APIRouter()


@router.get("/{user_id}/{pet_id}")
async def generate_single_pet_report(
    user_id: UUID,
    pet_id: UUID,
    report_service: ReportService = Depends(get_report_service),
) -> SinglePetReport:
    return await report_service.generate_single_pet_report(user_id, pet_id)


@router.get("/{user_id}")
async def get_or_generate_general_report(
    user_id: UUID,
    report_service: ReportService = Depends(get_report_service),
) -> ReportOut:
    return await report_service.get_or_generate_general_report(user_id)
