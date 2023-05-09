import sqlite3

DATABASE_NAME = "PatientRecords.db"


def get_db():
    conn = sqlite3.connect(DATABASE_NAME)
    return conn


def create_tables():
    users = ["create table If not exists Users(Id INTEGER Primary Key AutoIncrement, Username TEXT, Password TEXT, Email TEXT)"]
    tables = ["create table If not exists Records(Id INTEGER Primary Key AutoIncrement, PatientName TEXT, PatientAge INTEGER, PatientDisease TEXT, PatientContact NUMBER)"]
    db = get_db()
    cursor = db.cursor()
    for table in tables:
        cursor.execute(table)
    for user in users:
        cursor.execute(user)
