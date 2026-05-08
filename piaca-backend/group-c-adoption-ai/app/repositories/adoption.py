from fastapi import Depends
from sqlalchemy.orm import Session

from app.dependencies.database import piaca_db
from app.schemas.adoption import Adoption


class AdoptionRepository:
    def __init__(
        self,
        session: Session,
    ):
        self.session = session

    def read_many_adoptions(self) -> list[Adoption]:
        return [Adoption(_id="123456789", pet_name="mel")]

    def read_adoptions_by_ong(self, ong_id: str) -> list[Adoption]:
        return []

    def read_adoptions_by_user(self, user_id: str) -> list[Adoption]:
        return []

    def read_adoption_by_id(self, adoption_id: str) -> Adoption | None:
        return None


def get_adoption_repo(
    session: Session = Depends(piaca_db.get_session),
) -> AdoptionRepository:
    return AdoptionRepository(session=session)
