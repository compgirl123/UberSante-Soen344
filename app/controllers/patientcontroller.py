import sqlite3
import sqlite3 as mysql
import sqlite3 as sql
import sys
from sqlite3 import Error
import app.classes.database_container
from app.common_definitions.common_paths import PATH_TO_DATABASE
from app.controllers.patientcontroller import *
from app.classes.database_container import DatabaseContainer as db


class Patientcontroller:

    def patient_table(self, name):

        '''
        Creating Arrays to Store the values of each column for the Doctor Table
        '''

        ids = []
        last_names = []
        first_names = []
        birthdays = []
        genders = []
        emails = []
        phone_numbers = []
        ages = []
        health_cards = []
        addresses=[]

        table_creation_dict = {"patient": "SELECT id,last_name,first_name,birthday,gender,phone_number,email,address,age,health_card FROM patient;"}
        database = app.classes.database_container.DatabaseContainer.get_instance()

        for table_name, table_sql in table_creation_dict.items():
            database.execute_query(table_sql)

        results = database.execute_query("SELECT id,last_name,first_name,birthday,gender,phone_number,email,address,age,health_card FROM patient;")

        for row in database.execute_query("SELECT id,last_name,first_name,birthday,gender,phone_number,email,address,age,health_card FROM patient;"):
            ids.append(row["id"])
            last_names.append(row["last_name"])
            first_names.append(row["first_name"])
            birthdays.append(row["birthday"])
            genders.append(row["gender"])
            phone_numbers.append(row["phone_number"])
            emails.append(row["email"])
            ages.append(row["age"])
            addresses.append(row["address"])
            health_cards.append(row["health_card"])

        values_from_db = tuple(list(zip(ids,last_names,first_names,birthdays,genders,phone_numbers,emails,ages,addresses,health_cards)))
        return values_from_db

    def validatedornot(self, validation):
        return 0

    def user(self,health_card,phone_number):
        '''
               Creating Arrays to Store the values of each column for the Patient Table
        '''

        ids = []
        last_names = []
        first_names = []
        birthdays = []
        genders = []
        emails = []
        phone_numbers = []
        ages = []
        health_cards = []
        addresses=[]

        get_query = "SELECT * FROM patient WHERE health_card =" + "'" + health_card + "'" + " AND phone_number=" + "'" + phone_number+ "'"
        get_everything = "SELECT id,last_name,first_name,birthday,gender,phone_number,email,address,age,health_card FROM patient;"
        table_creation_dict = {"patient":  get_query}
        database = app.classes.database_container.DatabaseContainer.get_instance()

        for table_name, table_sql in table_creation_dict.items():
            database.execute_query(table_sql)

        results = database.execute_query(get_query)

        for row in database.execute_query(get_query):
            ids.append(row["id"])
            last_names.append(row["last_name"])
            first_names.append(row["first_name"])
            birthdays.append(row["birthday"])
            genders.append(row["gender"])
            phone_numbers.append(row["phone_number"])
            emails.append(row["email"])
            ages.append(row["age"])
            addresses.append(row["address"])
            health_cards.append(row["health_card"])

        values_from_db = tuple(list(zip(ids,last_names,first_names,birthdays,genders,phone_numbers,emails,ages,addresses,health_cards)))

        # if the values from the query work [id and password], then this should be validated
        if values_from_db:
            values_from_db = tuple(list(zip(ids,last_names,first_names,birthdays,genders,phone_numbers,emails,ages,addresses,health_cards)))
            #print("VALID")
        else:
            return
            #print("INVALID")

        return values_from_db



    def find_user(self, health_card, phone_number):
        # Make an sql  query to search for the name and pasword instead of seleting all

        self.health_card = health_card
        self.phone_number = phone_number

        #a = data()
        with mysql.connect("app/database/SOEN344_DATABASE.db") as con:

            loadhealth_card = ("select health_card from patient where health_card = '' "+health_card+" '' ")
            mycursor = con.cursor()
            mycursor.execute(a.health_card, loadhealth_card)
            health_cardcheck = mycursor.fetchone()

            loadphone_number = ("select phone_number from patient where phone_number = '%s'")
            mycursor2 = con.cursor()
            mycursor2.execute(a.phone_number,loadphone_number)
            phone_numbercheck = mycursor2.fetchone()

        if a.health_card == health_cardcheck and a.phone_number == phone_numbercheck:
            print ("welcome")

        else:
            print ("sorry please try again")
        con.commit()
        con.close()

    def patient_register(self, first_name, last_name,birthday,gender,phone_number,email,address,age,health_card):
        try:
            database = db.get_instance()
            #cur = con.cursor()
            database.execute_query("insert into patient(first_name, last_name,birthday,gender,phone_number,email,address,age,health_card) VALUES (?,?,?,?,?,?,?,?,?)",
                (first_name, last_name,birthday,gender,phone_number,email,address,age,health_card))
            database.commit_db()
            message = "Record Successfully added"
        except:
            message = "Error!!! Registration failed."
        finally:
            return message
            database.close_connection()

    def find_a_patient(self,healthcare_number):
        '''
            Finding the particular patient according to the healthcare # from the find nurse page
        '''
        database = db.get_instance()
        query = ""
        try:
            query = "SELECT * FROM patient WHERE health_card=" + "'" + healthcare_number +"'"
        except ValueError:
            query = ""

        cur = database.execute_query(query)
        data = cur.fetchall()
        d = tuple()
        for row in data:
            d = tuple((row["id"],row["first_name"], row["last_name"], row["birthday"], row["gender"],
                       row["phone_number"], row["email"],row["address"], row["age"],row["health_card"]))
        print(d)
        # returns a list of users
        return d

    def nurse_find_patient_by_clinic(self, healthcard_number):
        '''
             Nurse finds the particular patient according to the clinic the patient belongs to
        '''
        database = db.get_instance()

        query = "SELECT * FROM patient WHERE health_card=" + "'" + healthcard_number+"'"
        print(query)

        cur = database.execute_query(query)
        data = cur.fetchall()
        d = tuple()
        for row in data:
            d = tuple((row["first_name"],row["last_name"],row["birthday"],row["gender"],row["phone_number"]
            ,row["email"],row["address"],row["age"],row["health_card"]))
        # returns a list of users
        return d

    def deleteappointment(self, appointment_id):
            database = db.get_instance()
            print(appointment_id)
            appointment_id = str(appointment_id)
            query = "DELETE FROM appointment WHERE id =" + appointment_id
            database.execute_query(query)
            database.commit_db()
            message = "Availability Deleted"
            return message


    def getallappointmentsfordoctor(self, doctor_id):
        database = db.get_instance()
        query = "SELECT * FROM appointment WHERE doctor_id=" + str(doctor_id)
        print(query)
        queryexecute = database.execute_query(query)
        data = queryexecute.fetchall()
        return data


    def get_patient_name_from_id(self,doctor_id):
        database = db.get_instance()
        query = "SELECT patient.first_name, patient.last_name FROM patient INNER JOIN appointment ON patient.id = appointment.patient_id WHERE appointment.doctor_id = ""'" + str(doctor_id) + "'"""

        cur = database.execute_query(query)

        data = cur.fetchall()
        firstnames = []
        lastnames = []
        d = tuple()

        for row in data:
            #print(doctor.first_name)
            firstnames.append(row["first_name"])
            lastnames.append(row["last_name"])
            #d = tuple((row["speciality"]))
        d = tuple(list(zip(firstnames,lastnames)))

        # returns a list of users
        return d
