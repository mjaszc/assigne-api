from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import schemas.project_schema as project_schema
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


@router.post("/", response_model=project_schema.Project)
async def create_project(
    project: project_schema.ProjectCreate, db: Session = Depends(get_db)
):
    return project_crud.create_project(db, project)


@router.get("/{id}", response_model=project_schema.Project)
async def get_project_by_id(id: int, db: Session = Depends(get_db)):
    project = project_crud.get_project_by_id(db, id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.get("/", response_model=List[project_schema.Project])
async def get_all_projects(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    projects = project_crud.get_all_projects(db, skip, limit)
    return projects


@router.put("/{id}", response_model=project_schema.Project)
async def update_project_by_id(
    id: int, project: project_schema.ProjectCreate, db: Session = Depends(get_db)
):
    project_id = project_crud.get_project_by_id(db, id)
    if not project_id:
        raise HTTPException(status_code=404, detail="Project not found")
    db_project = project_crud.update_project(db, id, project)
    return db_project
