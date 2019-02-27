import sqlite3
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

    def find_user(self, name, password):
        print("HELLOO")
        return 0
