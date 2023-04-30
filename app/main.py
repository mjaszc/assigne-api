from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from typing import List

import schemas
import project_crud as project_crud
from database import SessionLocal


app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    return {"message": "App is working!"}


@app.post("/projects/", response_model=schemas.Project)
async def create_project(project: schemas.ProjectCreate, db: Session = Depends(get_db)):
    return project_crud.create_project(db=db, project=project)


@app.get("/projects/{id}", response_model=schemas.Project)
async def get_project_by_id(id: int, db: Session = Depends(get_db)):
    project = project_crud.get_project_by_id(db=db, project_id=id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@app.get("/projects/", response_model=List[schemas.Project])
async def get_all_projects(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    projects = project_crud.get_all_projects(db, skip=skip, limit=limit)
    return projects
