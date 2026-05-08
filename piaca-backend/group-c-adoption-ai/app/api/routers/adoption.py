from fastapi import APIRouter, Depends, HTTPException
from app.services.adoption import AdoptionService, get_adoption_service
from app.schemas.adoption import Adoption

router = APIRouter()


@router.get("/")
def get_all_adoptions(
    adoption_service: AdoptionService = Depends(get_adoption_service)
) -> list[Adoption]:
    return adoption_service.list_all()


@router.get("/ong/{ong_id}")
def get_adoptions_by_ong(
    ong_id: str,
    adoption_service: AdoptionService = Depends(get_adoption_service),
) -> list[Adoption]:
    return adoption_service.list_by_ong(ong_id)


@router.get("/user/{user_id}")
def get_adoptions_by_user(
    user_id: str,
    adoption_service: AdoptionService = Depends(get_adoption_service),
) -> list[Adoption]:
    return adoption_service.list_by_user(user_id)


@router.get("/{adoption_id}")
def get_adoption(
    adoption_id: str,
    adoption_service: AdoptionService = Depends(get_adoption_service),
) -> Adoption:
    adoption = adoption_service.get_by_id(adoption_id)
    if adoption is None:
        raise HTTPException(status_code=404, detail="Adoption not found")
    return adoption
