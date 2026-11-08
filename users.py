
from fastapi import *
from pydantic import BaseModel
from db import get_db
import os

router = APIRouter()
default_avatar = "uploads/avatars/default.png"

class NewUser(BaseModel):
    name: str
    surname: str
    phone_num: str
    passwd: str
class LoginRequest(BaseModel):
    phone_num: str
    passwd: str
class EditNameRequest(BaseModel):
    name: str
    surname: str
class EditAdditionalInfoRequest(BaseModel):
    additional_contact: str
class EditPasswordRequest(BaseModel):
    current_passwd: str
    new_passwd: str

@router.get("/users")
def get():
    connection = get_db()
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, name, surname, phone_num, additional_contact, avatar FROM users")
        users = cursor.fetchall()
    connection.close()
    return users
@router.post("/users")
def add(user: NewUser):
    connection = get_db()
    with connection.cursor() as cursor:
        sql = "INSERT INTO users (name, surname, phone_num, passwd, additional_contact, avatar) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (
            user.name,
            user.surname,
            user.phone_num,
            user.passwd,
            "",
            default_avatar
        )
        cursor.execute(sql, values)
        new_id = cursor.lastrowid
    connection.commit()
    connection.close()
    return {"status": "add: success", "message": f"{new_id} ({user.name}) added to db"}
@router.post("/login")
def login(credentials: LoginRequest):
    connection = get_db()
    with connection.cursor() as cursor:
        sql = "SELECT passwd FROM users WHERE phone_num = %s"
        cursor.execute(sql, (credentials.phone_num,))
        user = cursor.fetchone()
    connection.close()
    if user is None: return {"status": "login: error", "message": "bitch theres no user w that phone_num"}
    if user['passwd'] == credentials.passwd: return {"status": "login: success"}
    else: return {"status": "login: error", "message": "YO MAMA SOOO FAT"}
@router.put("/users/{user_id}")
def edit_name(user_id: int, user_data: EditNameRequest):
    connection = get_db()
    with connection.cursor() as cursor:
        sql = "UPDATE users SET name = %s, surname = %s WHERE id = %s"
        values = (user_data.name, user_data.surname, user_id)
        cursor.execute(sql, values)
    connection.commit()
    connection.close()
    return {"status": "edit_name: success", "message": f"User {user_id} changed their name to {user_data.name}"}
@router.put("/users/{user_id}/additional-info")
def edit_additional_info(user_id: int, user_data: EditAdditionalInfoRequest):
    connection = get_db()
    with connection.cursor() as cursor:
        sql = "UPDATE users SET additional_contact = %s WHERE id = %s"
        values = (user_data.additional_contact, user_id)
        cursor.execute(sql, values)
    connection.commit()
    connection.close()
    return {"status": "edit_additional_info: success", "message": f"User {user_id} changed their additional info"}
@router.put("/users/{user_id}/password")
def edit_password(user_id: int, user_data: EditPasswordRequest):
    connection = get_db()
    with connection.cursor() as cursor:
        cursor.execute("SELECT passwd FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        if user is None:
            connection.close()
            return {"status": "edit_password: error", "message": f"User {user_id} not found"}
        if user['passwd'] != user_data.current_passwd:
            connection.close()
            return {"status": "edit_password: error", "message": "Current password is incorrect"}
        cursor.execute(
            "UPDATE users SET passwd = %s WHERE id = %s",
            (user_data.new_passwd, user_id)
        )
    connection.commit()
    connection.close()
    return {"status": "edit_password: success", "message": f"User {user_id} changed their password"}
@router.put("/users/{user_id}/avatar")
def edit_avatar(user_id: int, image: UploadFile = File(...)):
    connection = get_db()
    os.makedirs("uploads/avatars", exist_ok=True)
    extension = os.path.splitext(image.filename or "")[1]
    name = f"{user_id}{extension}"
    file_path = f"uploads/avatars/{name}"
    with connection.cursor() as cursor:
        cursor.execute("SELECT id FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        if user is None:
            connection.close()
            return {"status": "edit_avatar: error", "message": f"User {user_id} not found"}
        with open(file_path, "wb") as idk:
            idk.write(image.file.read())
        sql = "UPDATE users SET avatar = %s WHERE id = %s"
        cursor.execute(sql, (file_path, user_id))
    connection.commit()
    connection.close()
    return {"status": "edit_avatar: success", "message": f"User {user_id} changed their avatar"}