from fastapi import APIRouter

from app.api.api_v1.endpoints import user, skill, vacant


api_router = APIRouter()
api_router.include_router(user.router, prefix="/users", tags=["users"])
api_router.include_router(skill.router, prefix="/skills", tags=["skills"])
api_router.include_router(vacant.router, prefix="/vacants", tags=["vacants"])
