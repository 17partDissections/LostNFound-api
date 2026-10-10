from fastapi import FastAPI
from pydantic import BaseModel
import pymysql

app = FastAPI()

def get_db():
    return pymysql.connect(
        host='localhost', user='root', password='',
        database='LostNFound',
        cursorclass=pymysql.cursors.DictCursor
    )

class NewUser(BaseModel):
    name: str
    surname: str
    phone_num: str
    passwd: str
    hide_phone_num: bool
    additional_contact: str = ""

class LoginRequest(BaseModel):
    phone_num: str
    passwd: str

class EditNameRequest(BaseModel):
    name: str
    surname: str

@app.get("/users")
def get():
    connection = get_db()
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
    connection.close()
    return users

@app.post("/users")
def add(user: NewUser):
    connection = get_db()
    with connection.cursor() as cursor:
        sql = "INSERT INTO users (name, surname, phone_num, passwd, hide_phone_num, additional_contact) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (user.name, user.surname, user.phone_num, user.passwd, user.hide_phone_num, user.additional_contact)
        cursor.execute(sql, values)
        new_id = cursor.lastrowid
    connection.commit()
    connection.close()
    return {"status": "add: success", "message": f"{new_id} ({user.name}) added to db"}

@app.post("/login")
def login(credentials: LoginRequest):
    connection = get_db()
    with connection.cursor() as cursor:
        sql = "SELECT * FROM users WHERE phone_num = %s"
        cursor.execute(sql, (credentials.phone_num,))
        user = cursor.fetchone()
    connection.close()
    if user is None: return {"status": "login: error", "message": "bitch theres no user w that phone_num"}
    if user['passwd'] == credentials.passwd: return {"status": "login: success"}
    else:return {"status": "login: error", "message": "YO MAMA SOOO FAT"}

@app.put("/users/{user_id}")
def edit_name(user_id: int, user_data: EditNameRequest):
    connection = get_db()
    with connection.cursor() as cursor:
        sql = "UPDATE users SET name = %s, surname = %s WHERE id = %s"
        values = (user_data.name, user_data.surname, user_id)
        cursor.execute(sql, values)
    connection.commit()
    connection.close()
    return {"status": "edit_name: success", "message": f"User {user_id} changed their name to {user_data.name}"}
