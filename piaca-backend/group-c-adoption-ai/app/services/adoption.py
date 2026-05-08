from fastapi import Depends

from app.repositories.adoption import AdoptionRepository, get_adoption_repo
from app.schemas.adoption import Adoption


class AdoptionService:
    def __init__(self, repo: AdoptionRepository):
        self.repo = repo

    def list_all(self) -> list[Adoption]:
        # return self.repo.get_all() -- exemplo
        return [Adoption(_id="123abc", pet_name="apollo")]

    def list_by_ong(self, ong_id: str) -> list[Adoption]:
        return self.repo.read_adoptions_by_ong(ong_id)

    def list_by_user(self, user_id: str) -> list[Adoption]:
        return self.repo.read_adoptions_by_user(user_id)

    def get_by_id(self, adoption_id: str) -> Adoption | None:
        return self.repo.read_adoption_by_id(adoption_id)

    # should have a lot of other methods that will 
    # basically be the main logic for the routes

    # example: the whole logic for actually adopting 
    # (business logic here)


def get_adoption_service(
    repo: AdoptionRepository = Depends(get_adoption_repo),
) -> AdoptionService:
    return AdoptionService(repo=repo)
