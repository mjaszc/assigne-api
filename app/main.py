from fastapi import FastAPI
from app.api.api import api_router

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import timedelta

from app.db.database import SessionLocal
import app.schemas.user_schema as user_schema
import app.crud.user_crud as user_crud
import app.crud.log_crud as log_crud

from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi import Response
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from jose import JWTError

app = FastAPI(title="AssigneAPI")

# Deployment CORS
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/token", response_model=user_schema.Token)
def login_for_access_token(
    response: Response, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db),
):
    db_user = user_crud.get_user_by_username(db, form_data.username)

    if not db_user or not pwd_context.verify(form_data.password, db_user.password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    access_token = user_crud.create_access_token(data={"sub": form_data.username}, expires_delta=timedelta(minutes=15))
    refresh_token = user_crud.create_refresh_token(data={"sub": form_data.username})
    response = JSONResponse({"access_token": access_token, "token_type": "bearer"})
    response.set_cookie(key="refresh_token", value=refresh_token, httponly=True, expires=1 * 24 * 60 * 60)
    response.set_cookie(key="access_token", value=access_token, httponly=True)

    return response

@app.post("/refresh")
async def refresh_token(response: Response, refresh_token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        username = user_crud.decode_token(refresh_token)
        db_user = user_crud.get_user_by_username(db, username)
        if db_user is None:
            raise HTTPException(status_code=401, detail="Invalid username")
        access_token = user_crud.create_access_token(data={"sub": username}, expires_delta=timedelta(minutes=15))
        response.set_cookie(key="access_token", value=access_token, httponly=True)
        return {"access_token": access_token, "token_type": "bearer"}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")


@app.post("/register", response_model=user_schema.User)
def register(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    existing_user = user_crud.get_user(db, user.email, user.username)
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="User with this email or username already registered",
        )

    # Generating log to the database
    log_details = f"Registered user: {user.username}"
    log_crud.create_log(db, action="Register user", details=log_details)

    return user_crud.create_user(db, user)


app.include_router(api_router)
