from db import get_db

logged = False


def register(username, password, email):
    db = get_db()
    cursor = db.cursor()
    statement = "Insert into Users(Username, Password, Email) values (?, ?, ?)"
    cursor.execute(statement, [username, password, email])
    db.commit()
    return "User Registered Successfully"


def login(username, password):
    global logged
    try:
        db = get_db()
        cursor = db.cursor()
        statement = "Select * from Users where Username=?"
        cursor.execute(statement, [username])
        data = cursor.fetchone()
        if data[2] == password:
            logged = True
            return True
        else:
            return False
    except:
        return False


def add_record(name, age, disease, contact):
    if logged:
        db = get_db()
        cursor = db.cursor()
        statement = "Insert into Records(PatientName, PatientAge, PatientDisease, PatientContact) values (?, ?, ?, ?)"
        cursor.execute(statement, [name, age, disease, contact])
        db.commit()
        return "Record Added"
    else:
        return "First Login"


def read_record():
    if logged:
        db = get_db()
        cursor = db.cursor()
        statement = "Select * from Records"
        records = cursor.execute(statement).fetchall()
        if records:
            return records
        else:
            return "No Records Found"
    else:
        return "First Login"


def read_record_by_id(id):
    if logged:
        db = get_db()
        cursor = db.cursor()
        statement = "Select * from Records where Id=?"
        records = cursor.execute(statement, [id]).fetchall()
        if records:
            return records
        else:
            return "No Records Found"
    else:
        return "First Login"


def read_record_by_disease(disease):
    if logged:
        db = get_db()
        cursor = db.cursor()
        statement = "Select * from Records where PatientDisease = ?"
        records = cursor.execute(statement, [disease]).fetchall()
        if records:
            return records
        else:
            return "No Records Found"
    else:
        return "First Login"


def read_record_by_name(name):
    if logged:
        db = get_db()
        cursor = db.cursor()
        statement = "Select * from Records where PatientName = ?"
        records = cursor.execute(statement, [name]).fetchall()
        if records:
            return records
        else:
            return "No Records Found"
    else:
        return "First Login"



def read_record_by_character(character):
    if logged:
        db = get_db()
        cursor = db.cursor()
        statement = "Select * from Records where PatientName LIKE ?"
        records = cursor.execute(statement, [character+'%']).fetchall()
        if records:
            return records
        else:
            return "No Records Found"
    else:
        return "First Login"


def read_record_order_by_age():
    if logged:
        db = get_db()
        cursor = db.cursor()
        statement = "Select * from Records order by PatientAge"
        records = cursor.execute(statement).fetchall()
        if records:
            return records
        else:
            return "No Records Found"
    else:
        return "First Login"


def update_record(id, name, age, disease, contact):
    if logged:
        try:
            db = get_db()
            cursor = db.cursor()
            statement = "Update Records Set PatientName=?, PatientAge=?, PatientDisease=?, PatientContact=? where Id=?"
            cursor.execute(statement, [name, age, disease, contact, id])
            db.commit()
            return "Record Updated"
        except:
            print("Record does not exist")
    else:
        return "First Login"


def delete_record(id):
    if logged:
        try:
            db = get_db()
            cursor = db.cursor()
            statement = "Delete From Records where id = ?"
            cursor.execute(statement, [id])
            db.commit()
            return "Record Deleted"
        except:
            print("Record does not exist")
    else:
        return "First Login"


def logout():
    global logged
    if logged:
        logged = False
        return True
