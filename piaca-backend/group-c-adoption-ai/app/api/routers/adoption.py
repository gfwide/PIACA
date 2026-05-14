from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from app.services.adoption import AdoptionService, get_adoption_service
from app.schemas.adoption import Adoption, CreateAdoptionRequest, UpdateAdoptionStatusRequest
from app.schemas.shared.responses import CreatedResponse, UpdatedResponse

router = APIRouter()


@router.get("/", response_model=list[Adoption])
def get_all_adoptions(
    adoption_service: AdoptionService = Depends(get_adoption_service)
) -> list[Adoption]:
    return adoption_service.list_all()


@router.post("/{user_id}", response_model=CreatedResponse, status_code=201)
def register_interest(
    user_id: UUID,
    body: CreateAdoptionRequest,
    adoption_service: AdoptionService = Depends(get_adoption_service),
) -> CreatedResponse:
    try:
        return adoption_service.register_interest(user_id, body)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))


@router.patch("/{id}/user/{user_id}/cancel", response_model=UpdatedResponse)
def cancel_adoption_request(
    id: UUID,
    user_id: UUID,
    adoption_service: AdoptionService = Depends(get_adoption_service),
) -> UpdatedResponse:
    try:
        return adoption_service.cancel_adoption_request(id, user_id)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))


@router.patch("/{id}/status", response_model=UpdatedResponse)
def update_adoption_status(
    id: UUID,
    user_id: UUID,
    body: UpdateAdoptionStatusRequest,
    adoption_service: AdoptionService = Depends(get_adoption_service),
) -> UpdatedResponse:
    try:
        return adoption_service.update_adoption_status(id, user_id, body)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

