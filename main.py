from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import pymysql
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

def get_db():
    return pymysql.connect(
        host='localhost', user='root', password='',
        database='LostNFound',
        cursorclass=pymysql.cursors.DictCursor
    )