from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from typing import List

import schemas
import crud
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
    return crud.create_project(db=db, project=project)


@app.get("/projects/", response_model=List[schemas.Project])
async def get_all_projects(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    projects = crud.get_all_projects(db, skip=skip, limit=limit)
    return projects
