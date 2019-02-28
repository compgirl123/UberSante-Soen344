import sqlite3
import sqlite3 as mysql
import sys
from sqlite3 import Error
import app.classes.database_container
from app.common_definitions.common_paths import PATH_TO_DATABASE
from app.controllers.nursecontroller import *


class Nursecontroller:

    def nurse_table(self, name):

        '''
        Creating Arrays to Store the values of each column for the Nurse Table
        '''

        ids = []
        first_names = []
        last_names = []
        passwords = []
        access_ids = []

        table_creation_dict = {"nurses": """SELECT id,last_name,first_name,password,access_id FROM nurse;"""}
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
        print(values_from_db)
        return values_from_db

    def find_user(self, access_id, password):
        # Make an sql query to search for the name and pasword instead of seleting all 
        #print("HELLOO")
        #return 0
        
        self.access_id = input
        self.password = input

        a = data()
        with mysql.connect("app/database/SOEN344_DATABASE.db") as con:

            loadaccess_id = ("select access_id from nurse where access_id = '%s'")
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
        
