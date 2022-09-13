from typing import Sequence

from pydantic import BaseModel


class SkillBase(BaseModel):
    name: str


# Properties to receive via API on creation
class SkillCreate(SkillBase):
    ...


# Properties to receive via API on update
class SkillUpdate(SkillBase):
    ...


class SkillInDBBase(SkillBase):
    id: str = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class Skill(SkillInDBBase):
    pass


class SkillSearchResults(BaseModel):
    results: Sequence[Skill]
