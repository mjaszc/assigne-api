from fastapi import FastAPI
from app.api.api import api_router

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import timedelta

from app.db.database import SessionLocal
import app.schemas.user_schema as user_schema
import app.crud.user_crud as user_crud

from fastapi.security import OAuth2PasswordRequestForm

app = FastAPI(title="AssigneAPI")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/token", response_model=user_schema.Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    db_user = user_crud.get_user_by_username(db, form_data.username)

    if not db_user or not pwd_context.verify(form_data.password, db_user.password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    access_token_expires = timedelta(minutes=15)
    access_token = user_crud.create_access_token(
        data={"sub": db_user.username}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/register", response_model=user_schema.User)
def register(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    existing_user = user_crud.get_user(db, user.email, user.username)
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="User with this email or username already registered",
        )

    db_user = user_crud.create_user(db, user)
    return db_user


app.include_router(api_router)
