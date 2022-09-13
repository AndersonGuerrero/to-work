from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Any, Optional

from app import crud
from app.api import deps
from app.schemas.skill import (
    Skill,
    SkillCreate,
    SkillUpdate,
    SkillSearchResults
)

router = APIRouter()


@router.get("/{skill_id}", status_code=HTTPStatus.OK, response_model=Skill)
def fetch_skill(
    *,
    skill_id: str,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Fetch a single skill by ID
    """
    result = crud.skill.get(db=db, id=skill_id)
    if not result:
        # the exception is raised, not returned - you will get a validation
        # error otherwise.
        raise HTTPException(
            status_code=404, detail=f"Skill with ID {skill_id} not found"
        )

    return result


@router.get(
    "/search/",
    status_code=HTTPStatus.OK,
    response_model=SkillSearchResults
)
def search_skills(
    *,
    name: Optional[str] = Query(None, min_length=3, example="Python"),
    max_results: Optional[int] = 10,
    db: Session = Depends(deps.get_db),
) -> dict:
    """
    Search for skills based on name keyword
    """
    skills = crud.skill.get_multi(db=db, limit=max_results)
    if not name:
        return {"results": skills}

    results = filter(
        lambda skill: name.lower() in skill.name.lower(),
        skills
    )
    return {"results": list(results)[:max_results]}


@router.get(
    "/",
    status_code=HTTPStatus.OK,
    response_model=SkillSearchResults
)
def all_skills(
    *,
    max_results: Optional[int] = 10,
    db: Session = Depends(deps.get_db),
) -> dict:
    """
    Search all skills
    """
    skills = crud.skill.get_multi(db=db, limit=max_results)
    return {"results": skills}


@router.post("/", status_code=HTTPStatus.CREATED, response_model=Skill)
def create_skill(
    *, skill_in: SkillCreate, db: Session = Depends(deps.get_db)
) -> dict:
    """
    Create a new skill in the database.
    """
    db_skill = crud.skill.get_by_name(db=db, name=skill_in.name)
    if db_skill:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Skill name already registered"
        )
    skill = crud.skill.create(db=db, obj_in=skill_in)

    return skill


@router.put("/{skill_id}", status_code=HTTPStatus.OK, response_model=Skill)
def update_skill(
    *, skill_id: str, skill: SkillUpdate, db: Session = Depends(deps.get_db)
) -> dict:
    """
    Update skill in the database.
    """
    db_obj = crud.skill.get(db=db, id=skill_id)
    skill = crud.skill.update(db=db, db_obj=db_obj, obj_in=skill)
    return skill


@router.delete(
    "/{skill_id}",
    status_code=HTTPStatus.OK,
    response_model=Skill
)
def delete_skill(
    *,
    skill_id: str,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Delete a single skill by ID
    """
    db_skill = crud.skill.remove(db=db, id=skill_id)
    if not db_skill:
        raise HTTPException(
            status_code=404,
            detail="Skill not exists"
        )
    return db_skill
