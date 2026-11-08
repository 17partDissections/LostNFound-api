from fastapi import APIRouter, UploadFile, File, Form
from db import get_db
import shutil

router = APIRouter()

@router.get("/ads")
def get_all_ads():
    connection = get_db()
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM ads")
        ads = cursor.fetchall()
    connection.close()
    return ads
@router.post("/ads")
def add_ad(
        user: int = Form(...),
        title: str = Form(...),
        description: str = Form(...),
        archive: bool = Form(...),
        image: UploadFile = File(...)
):
    connection = get_db()
    with connection.cursor() as cursor:
        sql_insert = " INSERT INTO ads (owner, title, description, image, archive) VALUES (%s, %s, %s, '', %s) "
        cursor.execute(sql_insert, (user, title, description, archive))
        id = cursor.lastrowid
        name = f"{user}_{id}.{image.filename.split('.')[-1]}"
        file_path = f"uploads/{name}" #/home/user/LostNFound/uploads/{name}
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        sql_update = "UPDATE ads SET image = %s WHERE id = %s"
        cursor.execute(sql_update, (file_path, id))
    connection.commit()
    connection.close()
    return {"status": "ad: success", "message": f"ad {id} successfully added"}