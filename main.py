from flask import Flask, jsonify, request
import streamlit as st
import record_controller
from db import create_tables
import requests
import pandas as pd
import re


app = Flask(__name__)


st.title("Patient Records Management")

menu = ["SignUp", "SignIn"]
choice = st.sidebar.selectbox("Menu", menu)
if choice == "SignUp":
    username = st.text_input("Username", key="username1")
    password = st.text_input("Password", key="password1")
    email = st.text_input("Email")
    inputs = {"username": username, "password": password, "email": email}
    if st.button("Register"):
        length_error = len(password) < 8
        digit_error = re.search(r"\d", password) is None
        uppercase_error = re.search(r"[A-Z]", password) is None
        lowercase_error = re.search(r"[a-z]", password) is None
        symbol_error = re.search(r"[ @!#$%&'()*+,-./[\\\]^_`{|}~" + r'"]', password) is None
        password_ok = not (length_error or digit_error or uppercase_error or lowercase_error or symbol_error)
        if password_ok:
            res = requests.post(url="http://127.0.0.1:5000/v1/register", json=inputs)
            st.write(res.json())
        else:
            st.write("""A password is considered strong if it contains atleast:
        8 characters length,
        1 digit,
        1 symbol,
        1 uppercase letter,
        1 lowercase letter""")

elif choice == "SignIn":
    username = st.text_input("Username", key="username2")
    password = st.text_input("Password", key="password2")
    inputs = {"username": username, "password": password}
    if st.button("Login"):
        res = requests.post(url="http://127.0.0.1:5000/v1/login", json=inputs)
        counter = res.json()
        if not counter:
            st.write("Invalid Credentials")
        else:
            st.write("Login Successful")
            if counter:
                menu1 = ["None", "Add", "Read", "Update", "Delete"]
                choice1 = st.sidebar.selectbox("CRUD", menu1)
                if choice1 == "Add":
                    patient_name = st.text_input("Patient Name")
                    patient_age = st.number_input("Patient Age", min_value=0, step=1, format="%i")
                    patient_disease = st.text_input("Patient Disease")
                    patient_contact = st.number_input("Patient Contact", min_value=0, step=1, format="%i")
                    inputs = {"name": patient_name, "age": patient_age, "disease": patient_disease, "contact": patient_contact}
                    if st.button("Add"):
                        res = requests.post(url="http://127.0.0.1:5000/v1/add", json=inputs)
                        st.write(res.json())

                elif choice1 == "Read":
                    menu2 = ["None", "Read All Records", "Read Record by ID", "Read Records by Disease", "Read Records by Name", "Read Records by Character"]
                    choice2 = st.sidebar.selectbox("Read", menu2)

                    if choice2 == "Read All Records":
                        if st.button("Read All Records"):
                            response = requests.get("http://127.0.0.1:5000/v1/read")
                            if response.json() != "No Records Found":
                                data_table = pd.DataFrame(response.json())
                                data_table.columns = ['ID', 'Patient Name', 'Patient Age', 'Patient Disease', 'Patient Contact']
                                data_table.set_index('ID', inplace=True)
                                st.write(data_table)
                            else:
                                st.write("No Records Found")

                    elif choice2 == "Read Record by ID":
                        id = st.number_input("Enter ID", min_value=0, step=1, format="%i")
                        if st.button("Read Record by ID"):
                            response = requests.get(f"http://127.0.0.1:5000/v1/read_by_id/{id}")
                            if response.json() != "No Records Found":
                                data_table = pd.DataFrame(response.json())
                                data_table.columns = ['ID', 'Patient Name', 'Patient Age', 'Patient Disease', 'Patient Contact']
                                data_table.set_index('ID', inplace=True)
                                st.write(data_table)
                            else:
                                st.write("No Records Found")

                    elif choice2 == "Read Records by Disease":
                        patient_disease = st.text_input("Disease")
                        if st.button("Read Records by Disease"):
                            response = requests.get(f"http://127.0.0.1:5000/v1/read_by_disease/{patient_disease}")
                            if response.json() != "No Records Found":
                                data_table = pd.DataFrame(response.json())
                                data_table.columns = ['ID', 'Patient Name', 'Patient Age', 'Patient Disease', 'Patient Contact']
                                data_table.set_index('ID', inplace=True)
                                st.write(data_table)
                            else:
                                st.write("No Records Found")

                    elif choice2 == "Read Records by Name":
                        patient_name = st.text_input("Name")
                        if st.button("Read Records by Name"):
                            response = requests.get(f"http://127.0.0.1:5000/v1/read_by_name/{patient_name}")
                            if response.json() != "No Records Found":
                                data_table = pd.DataFrame(response.json())
                                data_table.columns = ['ID', 'Patient Name', 'Patient Age', 'Patient Disease', 'Patient Contact']
                                data_table.set_index('ID', inplace=True)
                                st.write(data_table)
                            else:
                                st.write("No Records Found")

                    elif choice2 == "Read Records by Character":
                        character = st.text_input("Character")
                        if st.button("Read Records by Character"):
                            response = requests.get(f"http://127.0.0.1:5000/v1/read_by_character/{character}")
                            if response.json() != "No Records Found":
                                data_table = pd.DataFrame(response.json())
                                data_table.columns = ['ID', 'Patient Name', 'Patient Age', 'Patient Disease', 'Patient Contact']
                                data_table.set_index('ID', inplace=True)
                                st.write(data_table)
                            else:
                                st.write("No Records Found")

                elif choice1 == "Update":
                    id = st.number_input("Enter ID", min_value=0, step=1, format="%i")
                    if st.button("Read Record by ID"):
                        response = requests.get(f"http://127.0.0.1:5000/v1/read_by_id/{id}")
                        if response.json() != "No Records Found":
                            data_table = pd.DataFrame(response.json())
                            data_table.columns = ['ID', 'Patient Name', 'Patient Age', 'Patient Disease', 'Patient Contact']
                            data_table.set_index('ID', inplace=True)
                            name = st.text_input("Patient Name", data_table['Patient Name'].loc[data_table.index[0]])
                            age = st.text_input("Patient Age", data_table['Patient Age'].loc[data_table.index[0]])
                            disease = st.text_input("Patient Disease", data_table['Patient Disease'].loc[data_table.index[0]])
                            contact = st.text_input("Patient Contact", data_table['Patient Contact'].loc[data_table.index[0]])
                            inputs = {"name": name, "age": age, "disease": disease, "contact": contact}
                            if st.button("Update Record"):
                                res = requests.put(f"http://127.0.0.1:5000/v1/update/{id}", json=inputs)
                                st.write(res.json())
                        else:
                            st.write("No Records Found")

                elif choice1 == "Delete":
                    id = st.number_input("Enter ID", min_value=0, step=1, format="%i")
                    if st.button("Delete Record"):
                        response = requests.delete(f"http://127.0.0.1:5000/v1/delete/{id}")
                        st.write(response.json())

elif choice == "SignOut":
    if st.button("Logout"):
        response = requests.get("http://127.0.0.1:5000/v1/logout")
        st.write(response.text)
        counter1 = response.json()
        if counter1:
            st.write("Logged Out")


@app.route("/v1/register", methods=["POST"])
def register():
    user_details = request.get_json()
    username = user_details["username"]
    password = user_details["password"]
    email = user_details["email"]
    result = record_controller.register(username, password, email)
    return jsonify(result)


@app.route("/v1/login", methods=["POST"])
def login():
    user_details = request.get_json()
    username = user_details["username"]
    password = user_details["password"]
    result = record_controller.login(username, password)
    return jsonify(result)


@app.route("/v1/add", methods=["POST"])
def add_record():
    record_details = request.get_json()
    name = record_details["name"]
    age = record_details["age"]
    disease = record_details["disease"]
    contact = record_details["contact"]
    result = record_controller.add_record(name, age, disease, contact)
    return jsonify(result)


@app.route("/v1/read", methods=["GET"])
def read_records():
    result = record_controller.read_record()
    return jsonify(result)


@app.route("/v1/read_by_id/<id>", methods=["GET"])
def read_records_by_id(id):
    result = record_controller.read_record_by_id(id)
    return jsonify(result)


@app.route("/v1/read_by_disease/<disease>", methods=["GET"])
def read_records_by_disease(disease):
    result = record_controller.read_record_by_disease(disease)
    return jsonify(result)


@app.route("/v1/read_by_name/<name>", methods=["GET"])
def read_records_by_name(name):
    result = record_controller.read_record_by_name(name)
    return jsonify(result)


@app.route("/v1/read_by_character/<character>", methods=["GET"])
def read_records_by_character(character):
    result = record_controller.read_record_by_character(character)
    return jsonify(result)


@app.route("/v1/read_order_by_age", methods=["GET"])
def read_records_order_by_age():
    result = record_controller.read_record_order_by_age()
    return jsonify(result)


@app.route("/v1/update/<id>", methods=["PUT"])
def update_record(id):
    record_details = request.get_json()
    name = record_details["name"]
    age = record_details["age"]
    disease = record_details["disease"]
    contact = record_details["contact"]
    result = record_controller.update_record(id, name, age, disease, contact)
    return jsonify(result)


@app.route("/v1/delete/<id>", methods=["DELETE"])
def delete_record(id):
    result = record_controller.delete_record(id)
    return jsonify(result)


@app.route("/v1/logout", methods=["GET"])
def logout():
    st.write("Reached")
    result = record_controller.logout()
    return jsonify(result)


if __name__ == "__main__":
    create_tables()
    app.run()
