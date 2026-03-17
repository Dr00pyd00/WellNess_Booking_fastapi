from fastapi import FastAPI

from app.core.config import app_settings


app = FastAPI()


@app.get("/")
def root():
    return {"message":f"host: {app_settings.db_url}"}


