from fastapi import FastAPI
from db.database import SessionLocal
from api.api import api_router

app = FastAPI(title="AssigneAPI")


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


app.include_router(api_router)
