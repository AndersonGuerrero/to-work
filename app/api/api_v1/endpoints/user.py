from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from typing import Any, Optional

from app import crud
from app.api import deps
from app.schemas.user import User, UserUpdate, UserCreate
from app.schemas.user_skill import UserSkill, UserSkillCreate
from app.schemas.vacant import VacantSearchResults


router = APIRouter()


@router.get("/{user_id}", status_code=HTTPStatus.OK, response_model=User)
def fetch_user(
    *,
    user_id: str,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Fetch a single user by ID
    """
    result = crud.user.get(db=db, id=user_id)
    if not result:
        # the exception is raised, not returned - you will get a validation
        # error otherwise.
        raise HTTPException(
            status_code=404, detail=f"User with ID {user_id} not found"
        )

    return result


@router.delete(
    "/{user_id}",
    status_code=HTTPStatus.OK,
    response_model=User
)
def delete_user(
    *,
    user_id: str,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Delete a single user by ID
    """
    db_user = crud.user.remove(db=db, id=user_id)
    if not db_user:
        raise HTTPException(
            status_code=404,
            detail="User not exists"
        )
    return db_user


@router.get(
    "/",
    status_code=HTTPStatus.OK
)
def search_users(
    *,
    first_name: Optional[str] = Query(None, min_length=3, example="Mario"),
    max_results: Optional[int] = 10,
    db: Session = Depends(deps.get_db),
) -> dict:
    """
    Search for users based on first_name keyword
    """
    users = crud.user.get_multi(db=db, limit=max_results)
    results = []
    for user in users:
        skills = [{skill.skill.name: skill.value}for skill in user.skills]
        user_data = jsonable_encoder(user)
        user_data['skills'] = skills
        if first_name:
            if first_name.lower() in user.first_name.lower():
                results.append(user_data)
        else:
            results.append(user_data)
    return {"results": results[:max_results]}


@router.post("/", status_code=HTTPStatus.CREATED, response_model=User)
def create_user(
    *, user_in: UserCreate, db: Session = Depends(deps.get_db)
) -> dict:
    """
    Create a new user in the database.
    """
    db_user = crud.user.get_by_email(db=db, email=user_in.email)
    if db_user:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Email already registered"
        )
    user = crud.user.create(db=db, obj_in=user_in)
    return user


@router.put("/{user_id}", status_code=HTTPStatus.OK, response_model=User)
def update_user(
    *, user_id: str, user_in: UserUpdate, db: Session = Depends(deps.get_db)
) -> dict:
    """
    Update user in the database.
    """
    db_obj = crud.user.get(db=db, id=user_id)
    user = crud.user.update(db=db, db_obj=db_obj, obj_in=user_in)
    return user


@router.post(
    "/{user_id}/add-skills/",
    status_code=HTTPStatus.CREATED,
    response_model=UserSkill
)
def add_skills(
    *, user_id: str,
    user_skill: UserSkillCreate,
    db: Session = Depends(deps.get_db)
) -> dict:
    """
    add skills to user.
    """
    db_skill = crud.skill.get(db=db, id=user_skill.skill_id)
    db_user = crud.user.get(db=db, id=user_id)
    if not db_skill or not db_user:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="the skill does not exist"
        )
    if user_skill.value <= 0 or user_skill.value > 10:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="skill range is 1 to 10"
        )
    db_obj = crud.user_skill.create(
        db=db,
        obj_in=UserSkill(**user_skill.dict(), user_id=user_id)
    )
    return db_obj


@router.delete(
    "/{user_id}/remove-skills/",
    status_code=HTTPStatus.OK,
    response_model=UserSkill
)
def remove_skills(
    *, user_id: str,
    skill_id: str,
    db: Session = Depends(deps.get_db)
) -> dict:
    """
    remove skills from user.
    """
    remove_skill = crud.user_skill.remove(
        db=db,
        user_id=user_id,
        skill_id=skill_id
    )
    if not remove_skill:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="the skill or user does not exist"
        )
    return remove_skill


@router.get(
    "/{user_id}/vacants/",
    status_code=HTTPStatus.OK,
    response_model=VacantSearchResults
)
def user_vacants(
    *, user_id: str,
    db: Session = Depends(deps.get_db)
) -> dict:
    """
    get vacants per user.
    """
    user = crud.user.get(
        db=db,
        id=user_id
    )
    skills = {}
    skill_ids = []
    valid_vacants = []
    for skill in user.skills:
        skill_ids.append(skill.skill_id)
        skills.update({skill.skill_id: skill.value})
    vacants = crud.vacant.filter_per_skills(
        db=db,
        skill_ids=skill_ids
    )
    for vacant in vacants:
        total_skills = len(vacant.required_skills)
        user_skills = 0
        user_skills_valid = 0
        for skill in vacant.required_skills:
            user_skill = skills.get(skill.skill_id)
            if user_skill:
                user_skills += 1
                if user_skill >= skill.value:
                    user_skills_valid += 1
        if (
            total_skills == user_skills
            and user_skills_valid >= int(total_skills / 2)
        ):
            valid_vacants.append(vacant)
    return {"results": valid_vacants}
