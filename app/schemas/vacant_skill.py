from pydantic import BaseModel

from .skill import Skill


class VacantSkillBase(BaseModel):
    vacant_id: str
    skill_id: str
    value: str


class VacantSkillCreate(BaseModel):
    skill_id: str
    value: int


class VacantSkillInDBBase(VacantSkillBase):

    class Config:
        orm_mode = True


class VacantSkill(VacantSkillInDBBase):
    pass


class VacantSkillList(BaseModel):
    value: int
    skill: Skill

    class Config:
        orm_mode = True
