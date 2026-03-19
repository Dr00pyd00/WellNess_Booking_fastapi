from fastapi import FastAPI

from app.core.config import app_settings
from app import all_models

# routers imports:
from app.users.router import router as users_router
from app.auth.router import router as auth_router


app = FastAPI()

# Routers Bindings:
app.include_router(users_router)
app.include_router(auth_router)


@app.get("/")
def root():
    return {"message":f"host: {app_settings.db_url}"}


