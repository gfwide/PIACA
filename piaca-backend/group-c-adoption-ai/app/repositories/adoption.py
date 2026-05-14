from fastapi import Depends
from sqlalchemy.orm import Session
from datetime import datetime
from uuid import UUID, uuid4

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

    def create_interest(self, user_id: UUID, pet_id: UUID, message: str | None):
        # In a real implementation this would persist to the DB and return created record info
        new_id = uuid4()
        return {"id": new_id, "created_at": datetime.utcnow()}

    def cancel_interest(self, adoption_id: UUID, user_id: UUID):
        # In a real implementation this would validate ownership and update the persisted status
        return {
            "id": adoption_id,
            "updated_at": datetime.utcnow(),
            "function_response": {"status": "cancelado", "user_id": str(user_id)},
        }

    def update_status(self, adoption_id: UUID, status: int, user_id: UUID):
        # In a real implementation this would validate permissions and persist the new status.
        return {
            "id": adoption_id,
            "updated_at": datetime.utcnow(),
            "function_response": {
                "status": status,
                "user_id": str(user_id),
            },
        }


def get_adoption_repo(
    session: Session = Depends(piaca_db.get_session),
) -> AdoptionRepository:
    return AdoptionRepository(session=session)
