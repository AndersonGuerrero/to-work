from pydantic import BaseModel

from .skill import Skill


class UserSkillBase(BaseModel):
    user_id: str
    skill_id: str
    value: str


class UserSkillCreate(BaseModel):
    skill_id: str
    value: int


class UserSkillInDBBase(UserSkillBase):

    class Config:
        orm_mode = True


class UserSkill(UserSkillInDBBase):
    pass


class UserSkillList(BaseModel):
    value: int
    skill = Skill

    class Config:
        orm_mode = True
