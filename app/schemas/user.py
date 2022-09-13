from typing import Optional, List

from pydantic import BaseModel, EmailStr

from .user_skill import UserSkill


class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr = None
    years_previous_experience: int


class UserAddSkills(BaseModel):
    skills: List[str] = []


# Properties to receive via API on creation
class UserCreate(UserBase):
    email: EmailStr


# Properties to receive via API on update
class UserUpdate(UserBase):
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[EmailStr] = None
    years_previous_experience: Optional[int]


class UserInDBBase(UserBase):
    id: str = None
    skills: List[UserSkill] = []

    class Config:
        orm_mode = True


# Additional properties to return via API
class User(UserInDBBase):
    pass
