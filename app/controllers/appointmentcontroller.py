import sqlite3
import sqlite3 as mysql
import sys
from sqlite3 import Error
import app.classes.database_container
from app.common_definitions.common_paths import PATH_TO_DATABASE
from app.controllers.nursecontroller import *


class AppointmentController:
    def isAvailable(doctor_speciality, appointment_date, start_time, end_time):
        conn = connect_database()
        # If no doctor is available
        if (find_doctor(conn, doctor_speciality, appointment_date, start_time, end_time)) == false:
            return false

        # If no room is available
        elif (find_room(conn, appointment_date, start_time, end_time) == false):
            return false
        
        else:
            return true
        

    def create_appointment(doctor_speciality, patient_id, appointment_date, start_time, end_time):
        conn = connect_database()
        doctor_id = find_doctor(conn, doctor_speciality, appointment_date, start_time, end_time)
        if doctor_id == false:
            raise Exception('No doctor is available!')
        appointment_room = find_room(conn, appointment_date, start_time, end_time)
        if appointment_room == false:
            raise Exception('No room is available!')
        appointment_status = "Approved"
        appointment_type = getappointment_type(start_time, end_time)
        finalize_appointment(conn, appointment_room, appointment_type, appointment_status, appointment_date, start_time, end_time, patient_id, doctor_id)

    def getappointment_type(start_time, end_time):
        def get_sec(time_str):
            h, m, s = time_str.split(':')
            return int(h) * 3600 + int(m) * 60 + int(s)
        start = get_sec(start_time)
        end = get_sec(end_time)
        if (end - start) == 1200:
            return "Regular"
        elif (end - start) == 3600:
            return "Annual"
        else:
            return "Special"


    def find_room(conn, appointment_date, start_time, end_time):
        query = "SELECT appointment_room FROM appointment WHERE appointment_date=? AND start_time>=? AND end_time<=?"
        query2 = "SELECT id FROM room"
        conn.execute(query, (appointment_date, start_time, end_time))
        occupied = conn.fetchall()
        conn.execute(query2,())
        availableRooms = conn.fetchall()
        for room in availableRooms:
            if room in occupied:
                availableRooms.remove(room)
        if availableRooms != []:
            return availableRooms[0]
        else:
            return false

    def find_doctor(conn, doctor_speciality, appointment_date, start_time, end_time):
        query = "SELECT id FROM doctor WHERE speciality=?"
        query2 = "SELECT doctor_id FROM doctoravailability WHERE date=? AND start_time<=? AND end_time>=?"
        conn.execute(query,(doctor_speciality))
        specialists = conn.fetchall()
        conn.execute(query2,(appointment_date, start_time, end_time))
        availableDoctors = conn.fetchall()
        for specialist in specialists:
            if specialist in availableDoctors:
                return specialist
        return false
        

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
            query = "INSERT INTO appointment(appointment_room, appointment_type, appointment_status, appointment_date, start_time, end_time, patient_id, doctor_id) VALUES (?,?,?,?,?,?,?,?)"
            item = (appointment_room, appointment_type, appointment_status, appointment_date, start_time, end_time, patient_id, doctor_id)
            c.execute(query, item)
            return true

        except Error as e:
            print(e)
            return false

    def find_appointment(doctor_id, appointment_date):
        get_query = "SELECT * FROM appointment WHERE doctor_id ='" + doctor_id + "' AND appointment_date='" + appointment_date + "'"
