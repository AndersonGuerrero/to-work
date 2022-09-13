from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models import UserSkill
from app.schemas.skill import SkillCreate, SkillUpdate


class CRUDUserSkill(CRUDBase[UserSkill, SkillCreate, SkillUpdate]):

    def remove(
        self, db: Session,
        *,
        user_id: str,
        skill_id: str
    ) -> UserSkill:
        obj = db.query(UserSkill).filter(
            UserSkill.user_id == user_id,
            UserSkill.skill_id == skill_id
        ).first()
        if obj:
            db.delete(obj)
            db.commit()
            return obj

user_skill = CRUDUserSkill(UserSkill)
