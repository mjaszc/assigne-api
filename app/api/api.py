from fastapi import APIRouter
from app.api.routers import project_router, user_router, task_router, discussion_router

api_router = APIRouter()

api_router.include_router(project_router.router, tags=["projects"])
api_router.include_router(task_router.router, tags=["tasks"])
api_router.include_router(discussion_router.router, tags=["task discussions"])
api_router.include_router(user_router.router, tags=["users"])
