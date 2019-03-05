import sqlite3
import sqlite3 as mysql
import sys
from sqlite3 import Error
import app.classes.database_container
from app.common_definitions.common_paths import PATH_TO_DATABASE
from app.controllers.nursecontroller import *


class AppointmentController:
    def connect_database():
        try:
            conn = sqlite3.connect('./database/SOEN344_DATABASE.db')
            return conn
        except Error as e:
            print(e)
            return None
            
    def finalize_appointment(conn, appointment_room, appointment_type, appointment_status, appointment_date, start_time, end_time, patient_id, doctor_id):
        try:
            c = conn.cursor()
            query = '''INSERT INTO appointment_table(appointment_room, appointment_type, appointment_status, appointment_date, start_time, end_time, patient_id, doctor_id) VALUES (?,?,?,?,?,?,?,?)'''
            item = (appointment_room, appointment_type, appointment_status, appointment_date, start_time, end_time, patient_id, doctor_id)
            c.execute(query, item)
            return true

        except Error as e:
            print(e)
            return false

    def find_appointment(doctor_id, appointment_date):
        get_query = "SELECT * FROM appointment_table WHERE doctor_id ='" + doctor_id + "' AND appointment_date='" + appointment_date + "'"