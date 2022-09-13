from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models import Skill
from app.schemas.skill import SkillCreate, SkillUpdate


class CRUDSkill(CRUDBase[Skill, SkillCreate, SkillUpdate]):

    def get_by_name(self, db: Session, *, name: str) -> Optional[Skill]:
        return db.query(Skill).filter(Skill.name == name).first()

    def filter_by_ids(self, db: Session, *, skill_ids: list) -> Optional[Skill]:
        return db.query(Skill).filter(Skill.id.in_(skill_ids)).all()

    def update(
        self,
        db: Session,
        *,
        db_obj: Skill,
        obj_in: Union[SkillUpdate, Dict[str, Any]]
    ) -> Skill:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        return super().update(db, db_obj=db_obj, obj_in=update_data)

skill = CRUDSkill(Skill)
