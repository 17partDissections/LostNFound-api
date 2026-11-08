from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import users
import ads

api = FastAPI()
api.include_router(users.router)
api.include_router(ads.router)

api.mount(
    "/uploads",
    StaticFiles(directory="uploads"),
    name="uploads"
)