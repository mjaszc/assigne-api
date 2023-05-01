from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import schemas.project_schemas as project_schemas
import crud.project_crud as project_crud
from db.database import SessionLocal

router = APIRouter(prefix="/api/v1/projects")


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=project_schemas.Project)
async def create_project(
    project: project_schemas.ProjectCreate, db: Session = Depends(get_db)
):
    return project_crud.create_project(db=db, project=project)


@router.get("/{id}", response_model=project_schemas.Project)
async def get_project_by_id(id: int, db: Session = Depends(get_db)):
    project = project_crud.get_project_by_id(db=db, project_id=id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.get("/", response_model=List[project_schemas.Project])
async def get_all_projects(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    projects = project_crud.get_all_projects(db, skip=skip, limit=limit)
    return projects
