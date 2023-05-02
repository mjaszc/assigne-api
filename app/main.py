from fastapi import FastAPI
from app.api.api import api_router

app = FastAPI(title="AssigneAPI")


@app.get("/")
async def root():
    return {"message": "App is working!"}


app.include_router(api_router)
