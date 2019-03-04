import sqlite3
import sqlite3 as mysql
import sqlite3 as sql
import sys
from sqlite3 import Error
import app.classes.database_container
from app.common_definitions.common_paths import PATH_TO_DATABASE
from app.controllers.doctorcontroller import *


class Doctorcontroller:

    def doctor_table(self, name):

        '''
        Creating Arrays to Store the values of each column for the Doctor Table
        '''

        ids = []
        last_names = []
        first_names = []
        specialties = []
        cities = []
        passwords = []
        permit_numbers = []

        table_creation_dict = {"doctor": "SELECT id,last_name,first_name,speciality,city,password,permit_number FROM doctor;"}
        database = app.classes.database_container.DatabaseContainer.get_instance()

        for table_name, table_sql in table_creation_dict.items():
            database.execute_query(table_sql)

        results = database.execute_query("SELECT id,last_name,first_name,speciality,city,password,permit_number FROM doctor;")

        for row in database.execute_query("SELECT id,last_name,first_name,speciality,city,password,permit_number FROM doctor;"):
            ids.append(row["id"])
            last_names.append(row["last_name"])
            first_names.append(row["first_name"])
            specialties.append(row["speciality"])
            cities.append(row["city"])
            passwords.append(row["password"])
            permit_numbers.append(row["permit_number"])

        values_from_db = tuple(list(zip(ids,last_names,first_names,specialties,cities,passwords,passwords,permit_numbers)))
        #print(values_from_db)
        return values_from_db

    def validatedornot(self, validation):
        return 0

    def user(self,permit_number,password):
        '''
               Creating Arrays to Store the values of each column for the Nurse Table
        '''

        ids = []
        last_names = []
        first_names = []
        specialties = []
        cities = []
        passwords = []
        permit_numbers = []

        get_query = "SELECT * FROM doctor WHERE permit_number =" + "'" + permit_number + "'" + " AND password=" + "'" + password+ "'"
        get_everything = "SELECT id,last_name,first_name,speciality,city,password,permit_number FROM doctor;"
        print(get_query)
        table_creation_dict = {"doctor":  get_query}
        database = app.classes.database_container.DatabaseContainer.get_instance()

        for table_name, table_sql in table_creation_dict.items():
            database.execute_query(table_sql)

        results = database.execute_query(get_query)

        for row in database.execute_query(get_query):
            ids.append(row["id"])
            last_names.append(row["last_name"])
            first_names.append(row["first_name"])
            specialties.append(row["speciality"])
            cities.append(row["city"])
            passwords.append(row["password"])
            permit_numbers.append(row["permit_number"])

        values_from_db = tuple(list(zip(ids,last_names,first_names,specialties,cities,passwords,passwords,permit_numbers)))

        # if the values from the query work [id and password], then this should be validated
        if values_from_db:
            values_from_db = tuple(list(zip(ids,last_names,first_names,specialties,cities,passwords,passwords,permit_numbers)))
            #print("VALID")
        else:
            return
            #print("INVALID")

        #print(values_from_db)
        return values_from_db



    def find_user(self, permit_number, password):
        # Make an sql  query to search for the name and pasword instead of seleting all
        #print("HELLOO")
        #return 0
        
        self.permit_number = permit_number
        self.password = password

        #a = data()
        with mysql.connect("app/database/SOEN344_DATABASE.db") as con:

            loadpermit_number = ("select permit_number from doctor where permit_number = '' "+permit_number+" '' ")
            print(loadpermit_number)
            mycursor = con.cursor()
            mycursor.execute(a.permit_number, loadpermit_number)
            permit_numbercheck = mycursor.fetchone()
        
            loadpassword = ("select password from doctor where password = '%s'")
            mycursor2 = con.cursor()
            mycursor2.execute(a.password,loadpassword)
            passwordcheck = mycursor2.fetchone()

        if a.permit_number == permit_numbercheck and a.password == passwordcheck:
            print ("welcome")

        else:
            print ("sorry please try again")
        con.commit()
        con.close()

    def register_doctor(self, first_name, last_name, speciality, city, password, permit_number):
        try:
            database = app.classes.database_container.DatabaseContainer.get_instance()
            #cur = con.cursor()
            database.execute_query("insert into doctor(first_name, last_name, speciality, city, password, permit_number) VALUES (?,?,?,?,?,?)", (first_name, last_name, speciality, city, password, permit_number))
            database.commit_db()
            message = "Record Successfully added"
        except:
            message = "Error!!! Registration failed."
        finally:
            return message
            database.close_connection()