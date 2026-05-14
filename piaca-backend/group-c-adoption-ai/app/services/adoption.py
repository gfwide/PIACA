from __future__ import annotations

from datetime import datetime
from uuid import UUID
from fastapi import Depends

from app.repositories.adoption import AdoptionRepository, get_adoption_repo
from app.schemas.adoption import Adoption, CreateAdoptionRequest, UpdateAdoptionStatusRequest
from app.schemas.shared.responses import CreatedResponse, UpdatedResponse


class AdoptionService:
    def __init__(self, repo: AdoptionRepository):
        self.repo = repo

    def list_all(self) -> list[Adoption]:
        # return self.repo.get_all() -- exemplo
        return [Adoption(_id="123abc", pet_name="apollo")]

    def register_interest(self, user_id: UUID, data: CreateAdoptionRequest) -> CreatedResponse:
        repo_result = self.repo.create_interest(user_id, data.pet_id, data.message)
        return CreatedResponse(id=repo_result["id"], created_at=repo_result["created_at"], function_response=None)

    def cancel_adoption_request(self, adoption_id: UUID, user_id: UUID) -> UpdatedResponse:
        repo_result = self.repo.cancel_interest(adoption_id, user_id)
        return UpdatedResponse(
            id=repo_result["id"],
            updated_at=repo_result["updated_at"],
            function_response=repo_result["function_response"],
        )

    def update_adoption_status(
        self,
        adoption_id: UUID,
        user_id: UUID,
        data: UpdateAdoptionStatusRequest,
    ) -> UpdatedResponse:
        status_map = {
            "advance": 2,
            "reject": 3,
        }
        status = status_map[data.action]
        repo_result = self.repo.update_status(adoption_id, status, user_id)
        return UpdatedResponse(
            id=repo_result["id"],
            updated_at=repo_result["updated_at"],
            function_response=repo_result["function_response"],
        )


def get_adoption_service(
    repo: AdoptionRepository = Depends(get_adoption_repo),
) -> AdoptionService:
    return AdoptionService(repo=repo)
