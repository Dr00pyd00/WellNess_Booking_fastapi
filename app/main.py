from fastapi import FastAPI

from app.core.config import app_settings
from app import all_models

# routers imports:
from app.users.router import router as users_router
from app.auth.router import router as auth_router
from app.practitioners.router import router as pract_router


app = FastAPI()

# Routers Bindings:
app.include_router(users_router)
app.include_router(auth_router)
app.include_router(pract_router)


@app.get("/")
def root():
    return {"message":f"THis is WellNess ROOT!"}


