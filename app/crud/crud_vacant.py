from typing import Any, Dict, Union

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models import Vacant, VacantSkill
from app.schemas.vacant import VacantCreate, VacantUpdate


class CRUDVacant(CRUDBase[Vacant, VacantCreate, VacantUpdate]):

    def filter_per_skills(
        self, db: Session, *, skill_ids: str
    ) -> Vacant:
        objs = db.query(Vacant).join(VacantSkill).filter(
            VacantSkill.skill_id.in_(skill_ids)
        )
        return objs

    def update(
        self, db: Session, *,
        db_obj: Vacant,
        obj_in: Union[VacantUpdate, Dict[str, Any]]
    ) -> Vacant:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)

vacant = CRUDVacant(Vacant)
