import pymysql

def get_db():
    return pymysql.connect(
        host='localhost', user='user', password='passwd',
        database='db',
        cursorclass=pymysql.cursors.DictCursor
    )