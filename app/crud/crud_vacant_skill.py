from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models import VacantSkill
from app.schemas.vacant_skill import VacantSkillCreate


class CRUDVacantSkill(
    CRUDBase[VacantSkill, VacantSkillCreate, None]
):
    def filter_per_skills(
        self, db: Session, *, skill_ids: str
    ) -> VacantSkill:
        objs = db.query(VacantSkill).filter(
            VacantSkill.skill_id.in_(skill_ids)
        )
        return objs

    def remove(
        self, db: Session, *, vacant_id: str, skill_id: str
    ) -> VacantSkill:
        obj = db.query(VacantSkill).filter(
            VacantSkill.vacant_id == vacant_id,
            VacantSkill.skill_id == skill_id
        ).first()
        if obj:
            db.delete(obj)
            db.commit()
            return obj

vacant_skill = CRUDVacantSkill(VacantSkill)
