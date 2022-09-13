from typing import Optional, List, Sequence

from pydantic import BaseModel, HttpUrl

from app.helpers import CurrencyEnum
from .vacant_skill import VacantSkillList


class VacantBase(BaseModel):
    vacancy_link: HttpUrl = None
    position_name: str
    company_name: str
    salary: float
    currency = CurrencyEnum.USD


class VacantAddSkills(BaseModel):
    required_skills: List[str] = []


# Properties to receive via API on creation
class VacantCreate(VacantBase):
    currency: CurrencyEnum = str


# Properties to receive via API on update
class VacantUpdate(VacantBase):
    vacancy_link: Optional[HttpUrl] = str
    position_name: Optional[str]
    company_name: Optional[str]
    salary: Optional[float]
    currency: Optional[CurrencyEnum] = str


class VacantInDBBase(VacantBase):
    id: str = None
    required_skills: List[VacantSkillList] = []

    class Config:
        orm_mode = True


# Additional properties to return via API
class Vacant(VacantInDBBase):
    pass


class VacantSearchResults(BaseModel):
    results: Sequence[Vacant]
