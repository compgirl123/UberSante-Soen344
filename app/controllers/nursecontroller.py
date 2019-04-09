import sqlite3
import sqlite3 as mysql
import sys
from sqlite3 import Error
import app.classes.database_container
from app.common_definitions.common_paths import PATH_TO_DATABASE
from app.controllers.nursecontroller import *
from app.classes.database_container import DatabaseContainer as db

class Nursecontroller:

    def nurse_table(self, name):

        '''
                Gets the entire database of nurses. Used as a reference point function
        '''

        ids = []
        first_names = []
        last_names = []
        passwords = []
        access_ids = []

        table_creation_dict = {"nurses": "SELECT id,last_name,first_name,password,access_id FROM nurse;"}
        database = app.classes.database_container.DatabaseContainer.get_instance()

        for table_name, table_sql in table_creation_dict.items():
            database.execute_query(table_sql)

        results = database.execute_query("SELECT id,last_name,first_name,password,access_id FROM nurse;")

        for row in database.execute_query("SELECT id,first_name,last_name,password,access_id FROM nurse;"):
            ids.append(row["id"])
            first_names.append(row["first_name"])
            last_names.append(row["last_name"])
            passwords.append(row["password"])
            access_ids.append(row["access_id"])

        values_from_db = tuple(list(zip(ids,first_names, last_names,passwords,access_ids)))
        return values_from_db

    def validatedornot(self, validation):
        return 0

    def user(self,access_id,password):
        '''
               Returns all the information of the nurse that is validated upon login
        '''

        ids = []
        first_names = []
        last_names = []
        passwords = []
        access_ids = []

        get_query = "SELECT * FROM nurse WHERE access_id =" + "'" + access_id + "'" + " AND password=" + "'" + password+ "'"
        get_everything = "SELECT id,last_name,first_name,password,access_id FROM nurse"
        table_creation_dict = {"nurses":  get_query}
        database = app.classes.database_container.DatabaseContainer.get_instance()

        for table_name, table_sql in table_creation_dict.items():
            database.execute_query(table_sql)

        results = database.execute_query(get_query)

        for row in database.execute_query(get_query):
            ids.append(row["id"])
            first_names.append(row["first_name"])
            last_names.append(row["last_name"])
            passwords.append(row["password"])
            access_ids.append(row["access_id"])

        values_from_db = tuple(list(zip(ids, first_names, last_names, passwords, access_ids)))

        # if the values from the query work [id and password], then this should be validated
        if values_from_db:
            values_from_db = tuple(list(zip(ids, first_names, last_names, passwords, access_ids)))
            #print("VALID")
        else:
            return
            #print("INVALID")

        return values_from_db


    def find_user(self, access_id, password):
        # Make an sql  query to search for the name and pasword instead of seleting all

        self.access_id = access_id
        self.password = password

        #a = data()
        with mysql.connect("app/database/SOEN344_DATABASE.db") as con:

            loadaccess_id = ("select access_id from nurse where access_id = '' "+access_id+" '' ")
            mycursor = con.cursor()
            mycursor.execute(a.access_id, loadaccess_id)
            access_idcheck = mycursor.fetchone()

            loadpassword = ("select password from nurse where password = '%s'")
            mycursor2 = con.cursor()
            mycursor2.execute(a.password,loadpassword)
            passwordcheck = mycursor2.fetchone()

        if a.access_id == access_idcheck and a.password == passwordcheck:
            print ("welcome")

        else:
            print ("sorry please try again")
        con.commit()
        con.close()

    def nurse_full_name(self,user_id):
        '''
            Finding the particular patient according to the healthcare # from the find nurse page
        '''

        database = db.get_instance()
        query = "SELECT first_name, last_name FROM nurse WHERE access_id=" + "'" + user_id +"'"

        cur = database.execute_query(query)
        data = cur.fetchall()
        d = tuple()

        for row in data:
            d = tuple((row["first_name"], row["last_name"]))
        print(d)
        # returns a list of users
        return d

    def nurse_clinic(self,user_id):
        '''
            Finding the particular clinic that a nurse works at
        '''

        database = db.get_instance()
        query = "SELECT clinic_name FROM nurse WHERE access_id=" + "'" + user_id +"'"

        cur = database.execute_query(query)
        data = cur.fetchall()
        d = tuple()

        for row in data:
            d = row["clinic_name"]
        print(d)
        # returns a list of users
        return d
        
