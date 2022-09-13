from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from typing import Any, Optional

from app import crud
from app.api import deps
from app.schemas.vacant import Vacant, VacantUpdate, VacantCreate
from app.schemas.vacant_skill import VacantSkill, VacantSkillCreate


router = APIRouter()


@router.get("/{vacant_id}", status_code=HTTPStatus.OK, response_model=Vacant)
def fetch_vacant(
    *,
    vacant_id: str,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Fetch a single vacant by ID
    """
    result = crud.vacant.get(db=db, id=vacant_id)
    if not result:
        raise HTTPException(
            status_code=404,
            detail=f"Vacant with ID {vacant_id} not found"
        )
    return result


@router.delete(
    "/{vacant_id}",
    status_code=HTTPStatus.OK,
    response_model=Vacant
)
def delete_vacant(
    *,
    vacant_id: str,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Delete a single vacant by ID
    """
    db_vacant = crud.vacant.remove(db=db, id=vacant_id)
    if not db_vacant:
        raise HTTPException(
            status_code=404,
            detail="Vacant not exists"
        )
    return db_vacant


@router.get(
    "/",
    status_code=HTTPStatus.OK
)
def search_vacant(
    *,
    position_name: Optional[str] = Query(
        None,
        min_length=3,
        example="Python Dev"
    ),
    max_results: Optional[int] = 10,
    db: Session = Depends(deps.get_db),
) -> dict:
    """
    Search for vacants based on position_name keyword
    """
    vacants = crud.vacant.get_multi(db=db, limit=max_results)
    results = []
    for vacant in vacants:
        required_skills = [
            {skill.skill.name: skill.value}for skill in vacant.required_skills
        ]
        user_data = jsonable_encoder(vacant)
        user_data['required_skills'] = required_skills
        if position_name:
            if position_name.lower() in vacant.position_name.lower():
                results.append(user_data)
        else:
            results.append(user_data)
    return {"results": results[:max_results]}


@router.post("/", status_code=HTTPStatus.CREATED, response_model=Vacant)
def create_vacant(
    *, vacant_in: VacantCreate, db: Session = Depends(deps.get_db)
) -> dict:
    """
    Create a new vacant in the database.
    """
    vacant = crud.vacant.create(db=db, obj_in=vacant_in)
    return vacant


@router.put("/{vacant_id}", status_code=HTTPStatus.OK, response_model=Vacant)
def update_vacant(
    *, vacant_id: str,
    user_in: VacantUpdate,
    db: Session = Depends(deps.get_db)
) -> dict:
    """
    Update vacant in the database.
    """
    db_obj = crud.vacant.get(db=db, id=vacant_id)
    vacant = crud.vacant.update(db=db, db_obj=db_obj, obj_in=user_in)
    return vacant


@router.post(
    "/{vacant_id}/add-skills/",
    status_code=HTTPStatus.CREATED,
    response_model=VacantSkill
)
def add_skills(
    *, vacant_id: str,
    vacant_skill: VacantSkillCreate,
    db: Session = Depends(deps.get_db)
) -> dict:
    """
    add skills to vacant.
    """
    db_skill = crud.skill.get(db=db, id=vacant_skill.skill_id)
    db_vacant = crud.vacant.get(db=db, id=vacant_id)
    if not db_skill or not db_vacant:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="the skill or vacant does not exist"
        )
    if vacant_skill.value <= 0 or vacant_skill.value > 10:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="skill range is 1 to 10"
        )
    db_obj = crud.vacant_skill.create(
        db=db,
        obj_in=VacantSkill(**vacant_skill.dict(), vacant_id=vacant_id)
    )
    return db_obj


@router.delete(
    "/{vacant_id}/remove-skills/",
    status_code=HTTPStatus.OK,
    response_model=VacantSkill
)
def remove_skills(
    *, vacant_id: str,
    skill_id: str,
    db: Session = Depends(deps.get_db)
) -> dict:
    """
    remove skills from vacant.
    """
    remove_skill = crud.vacant_skill.remove(
        db=db,
        vacant_id=vacant_id,
        skill_id=skill_id
    )
    if not remove_skill:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="the skill or vacant does not exist"
        )
    return remove_skill
