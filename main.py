from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import users
import ads

api = FastAPI()

api.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://1566lostnfound.ru",
        "https://www.1566lostnfound.ru"
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"]
)

api.include_router(users.router)
api.include_router(ads.router)

api.mount(
    "/uploads",
    StaticFiles(directory="uploads"),
    name="uploads"
)