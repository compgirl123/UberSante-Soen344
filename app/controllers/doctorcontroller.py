import sqlite3
import sqlite3 as mysql
import sqlite3 as sql
import sys
import shutil
from sqlite3 import Error
import app.classes.database_container
from app.common_definitions.common_paths import PATH_TO_DATABASE
from app.controllers.doctorcontroller import *
from app.classes.database_container import DatabaseContainer as db


class Doctorcontroller:

    def doctor_table(self):

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

        for row in database.execute_query("SELECT DISTINCT id,last_name,first_name,speciality,city,password,permit_number FROM doctor;"):
            ids.append(row["id"])
            last_names.append(row["last_name"])
            first_names.append(row["first_name"])
            specialties.append(row["speciality"])
            cities.append(row["city"])
            passwords.append(row["password"])
            permit_numbers.append(row["permit_number"])

        values_from_db = tuple(list(zip(ids,last_names,first_names,specialties,cities,passwords,passwords,permit_numbers)))
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
        return values_from_db


    def find_user(self, permit_number, password):
        # Make an sql  query to search for the name and pasword instead of seleting all
        
        self.permit_number = permit_number
        self.password = password

        #a = data()
        with mysql.connect("app/database/SOEN344_DATABASE.db") as con:

            loadpermit_number = ("select permit_number from doctor where permit_number = '' "+permit_number+" '' ")
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

    def register_doctor(self, first_name, last_name, speciality, city, password, permit_number, clinic_name):
        try:
            database = db.get_instance()
            database.execute_query("insert into doctor(first_name, last_name, speciality, city, password, permit_number,clinic_name) VALUES (?,?,?,?,?,?,?)", (first_name, last_name, speciality, city, password, permit_number,clinic_name))
            database.commit_db()
            message = "Record Successfully added"
        except:
            message = "Error!!! Registration failed."
        finally:
            return message
            database.close_connection()

    def find_doctor_by_permit_number(self, permit_number):
        '''
             Finding the particular doctor according to the permit # from the find nurse page
        '''
        database = db.get_instance()
        try:
            val = int(permit_number)
            if (val > 0):
                query = "SELECT * FROM doctor WHERE permit_number=" + permit_number
            else:
                query = ""
        except ValueError:
            query = ""

        cur = database.execute_query(query)
        data = cur.fetchall()
        d = tuple()
        for row in data:
            d = tuple((row["first_name"],row["last_name"],row["speciality"],row["city"],row["permit_number"],row["password"]))
        # returns a list of users
        return d

    def nurse_find_doctor_by_clinic(self, permit_number, clinic_name):
        '''
            Nurse finds the particular doctor according to the clinic the doctor belongs to
        '''
        database = db.get_instance()
        
        query = "SELECT * FROM doctor WHERE permit_number=" + permit_number + " AND clinic_name="+"'"+ clinic_name+ "'"
        print(query)

        cur = database.execute_query(query)
        data = cur.fetchall()
        d = tuple()
        for row in data:
            d = tuple((row["first_name"],row["last_name"],row["speciality"],row["city"],row["permit_number"],row["clinic_name"]))
        # returns a list of users
        print(d)
        return d


    def find_doctor_id(self,permit_number):
        database = db.get_instance()
        query = "SELECT id FROM doctor WHERE permit_number=" + permit_number
        queryexecute = database.execute_query(query)
        data = queryexecute.fetchall()

        return str(data[0][0])

    def doctorappointmentbook(self, day, start_time_hour, start_time_minute, end_time_hour, end_time_minute, doctor_id, clinic_name):
        message = "Availabilities loaded"
        database = db.get_instance()
        _start_time_hour = int(start_time_hour)
        _start_time_minute = int(start_time_minute)

        _end_time_hour = int(end_time_hour)
        _end_time_minute = int(end_time_minute)
        start_time = str(start_time_hour) + ':' + str(start_time_minute)     
        end_time = str(end_time_hour) + ':' + str(end_time_minute) 
        doctor_id = str(doctor_id)


        if (_start_time_hour <= _end_time_hour and _start_time_minute < _end_time_minute) or (_start_time_hour < _end_time_hour):
            start_time = str(start_time_hour) + ':' + str(start_time_minute)     
            end_time = str(end_time_hour) + ':' + str(end_time_minute) 
            query3 = "SELECT COUNT(*) FROM doctoravailability WHERE date_day= '" + day + "' AND doctor_id=" + doctor_id + " AND clinic_name="+"'"+ clinic_name+ "'"
            cur = database.execute_query(query3)
            data1 = cur.fetchall()
            data1 = int(data1[0][0])
            print(data1)
            if data1 == 0:
                doctor_id = int(doctor_id)
                start_time = start_time + ":00"
                end_time = end_time + ":00"
                query2 = "insert into doctoravailability(date_day, start_time, end_time, doctor_id,clinic_name) VALUES (?,?,?,?,?)"
                database.execute_query(query2, (day, start_time, end_time,doctor_id, clinic_name))
                database.commit_db()
                print("hello")
                return "Availability Added"
            else:
                query = "SELECT * FROM doctoravailability WHERE date_day= '" + day + "' AND doctor_id=" + doctor_id + " AND clinic_name="+"'"+ clinic_name+ "'"
                cur = database.execute_query(query)
                data = cur.fetchall()
                count = 0

                for row in data:
                    start = row[2]
                    end = row[3]
                    if int(start[0:1]) == 8 or int(start[0:1]) == 9: 
                        start = '0' + start
                    if int(end[0:1]) == 8 or int(end[0:1]) == 9 :
                        end = '0' + end
                    print(start)
                    print(end)
                    if (_start_time_hour > int(end[0:2]) and _end_time_hour > int(end[0:2])) or \
                        (_start_time_hour < int(start[0:2]) and _end_time_hour < int(start[0:2])) or \
                        (_start_time_hour < int(start[0:2]) and _end_time_hour <= int(start[0:2]) and _end_time_minute <= int(start[3:5])) or \
                        (_start_time_hour >= int(end[0:2]) and _end_time_hour > int(end[0:2]) and _start_time_minute >= int(end[3:5])) or \
                        (_start_time_hour <= int(start[0:2]) and _end_time_hour <= int(start[0:2]) and _start_time_minute < int(start[3:5]) and _end_time_minute <= int(start[3:5])):
                        count += 1
                        print(count)
                        if count == data1:
                            start_time = start_time + ":00"
                            end_time = end_time + ":00"
                            query2 = "insert into doctoravailability(date_day, start_time, end_time, doctor_id,clinic_name) VALUES (?,?,?,?,?)"
                            database.execute_query(query2, (day, start_time, end_time,doctor_id,clinic_name))
                            database.commit_db()
                            message = "Availability Added"
                            return message
                   
                    
                return "Enter proper values"
        else:
            message = "Enter proper values!!!" 
        #query2 = "insert into doctoravailability(date_day, start_time, end_time, doctor_id) VALUES (?,?,?,?)"
        #database.execute_query(query2, (day, start_time, end_time,doctor_id ))
        #database.commit_db()
        return message

    def doctorgetallappointments(self, doctor_id,clinic_name):
        database = db.get_instance()
        query = "SELECT * FROM doctoravailability WHERE doctor_id=" + doctor_id + " AND clinic_name="+"'"+ clinic_name+ "'"
        queryexecute = database.execute_query(query)
        data = queryexecute.fetchall()
        return data

    def doctorgetclinic(self, doctor_id):
        database = db.get_instance()
        query = "SELECT clinic_name FROM doctor WHERE permit_number=" + doctor_id
        queryexecute = database.execute_query(query)
        data = queryexecute.fetchall()
        print(data)
        return data

    def deleteappointment(self, doctor_id,clinic_name):
        database = db.get_instance()
        print(doctor_id)
        doctor_id = str(doctor_id)
        query = "DELETE FROM doctoravailability WHERE id =" + doctor_id + " AND clinic_name="+"'"+ clinic_name+ "'"
        database.execute_query(query)
        database.commit_db()
        message = "Availability Deleted"
        return message
      
    def find_doctor_by_full_name(self, first_name, last_name):
        '''
             Finding the particular doctor according to their first and last name
        '''
        database = db.get_instance()
        query = "SELECT * FROM doctor WHERE first_name= ""'" + first_name + "'"" AND last_name= ""'" + last_name + "'"""

        cur = database.execute_query(query)
        data = cur.fetchall()
        d = tuple()
        for row in data:
            d = tuple((row["first_name"],row["last_name"],row["speciality"],row["city"],row["permit_number"],row["password"]))
        # returns a list of users
        return d

    def get_doctor_by_id(self,doctor_id):

        database = db.get_instance()
        query = "SELECT * FROM doctor WHERE id= ""'" + str(doctor_id) + "'"""

        cur = database.execute_query(query)
        data = cur.fetchall()
        d = tuple()
        for row in data:
            d = tuple((row["first_name"], row["last_name"], row["speciality"], row["city"], row["permit_number"],
                       row["password"]))
        # returns a list of users
        return d

    def get_doctor_by_specialty(self,doctor_specialty):
        database = db.get_instance()
        query = "SELECT * FROM doctor WHERE speciality= ""'" + str(doctor_specialty) + "'"""

        cur = database.execute_query(query)
        data = cur.fetchall()
        ids = []
        last_names = []
        first_names = []
        specialties = []
        cities = []
        passwords = []
        permit_numbers = []
        
        d = tuple()
        for row in data:
            ids.append(row["id"])
            last_names.append(row["last_name"])
            first_names.append(row["first_name"])
            specialties.append(row["speciality"])
            cities.append(row["city"])
            passwords.append(row["password"])
            permit_numbers.append(row["permit_number"])

        values_from_db = tuple(list(zip(ids,last_names,first_names,specialties,cities,passwords,passwords,permit_numbers)))
        '''doctors_list.append(row["first_name"], row["last_name"], row["speciality"], row["city"], row["permit_number"],
                       row["password"])'''
        #d = tuple((row["first_name"], row["last_name"], row["speciality"], row["city"], row["permit_number"],
                       #row["password"]))
        d = values_from_db
        # returns a list of users
        return d

       
       # A new function that will get the doctors works works at that clinic
    def get_doctor_by_clinic_name(self,doctor_clinic_name):
        database = db.get_instance()

        # Get all the doctor specialities information for the clinic
        query = "SELECT * FROM doctor WHERE clinic_name = ""'" + str(doctor_clinic_name) + "'"""

        cur = database.execute_query(query)
        data = cur.fetchall()
        ids = []
        last_names = []
        first_names = []
        specialties = []
        clinic_names = []
        cities = []
        passwords = []
        permit_numbers = []
        
        d = tuple()
        for row in data:
            ids.append(row["id"])
            last_names.append(row["last_name"])
            first_names.append(row["first_name"])
            specialties.append(row["speciality"])
            clinic_names.append(row["clinic_name"])
            cities.append(row["city"])
            passwords.append(row["password"])
            permit_numbers.append(row["permit_number"])

        values_from_db = tuple(list(zip(ids,last_names,first_names,specialties,clinic_names, cities,passwords,passwords,permit_numbers)))
        print(values_from_db)
        print()
        '''doctors_list.append(row["first_name"], row["last_name"], row["speciality"], row["clinic_name"], row["city"], row["permit_number"],
                    row["password"])'''
    
        #d = tuple((row["first_name"], row["last_name"], row["speciality"], row["clinic_name"], row["city"], row["permit_number"],
                    #row["password"]))
        d = values_from_db
        
        # returns a list of doctors
        return d
    
    def get_distinct_speciality(self):
        database = db.get_instance()
        query = "SELECT DISTINCT speciality FROM doctor"

        cur = database.execute_query(query)
        
        data = cur.fetchall()
        specialties = []
        d = tuple()
        for row in data:
            print(row["speciality"])
            specialties.append(row["speciality"])
            #d = tuple((row["speciality"]))
        d = tuple(specialties)
        # returns a list of users
        return d

    def get_doctor_name_from_id(self,patient_id):
        database = db.get_instance()
        query = "SELECT doctor.first_name, doctor.last_name FROM doctor INNER JOIN appointment ON doctor.id = appointment.doctor_id WHERE appointment.patient_id = ""'" + str(patient_id) + "'"""

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
        
