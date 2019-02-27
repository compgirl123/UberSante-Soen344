import sqlite3
import sys
from sqlite3 import Error
import app.classes.database_container
from app.common_definitions.common_paths import PATH_TO_DATABASE
from app.controllers.nursecontroller import *


class Nursecontroller:

    def nurse_table(self, name):
        table_creation_dict = {"nurses": """SELECT id,last_name,first_name,password,access_id FROM nurse;"""}
        database = app.classes.database_container.DatabaseContainer.get_instance()

        for table_name, table_sql in table_creation_dict.items():
            database.execute_query(table_sql)

        results = database.execute_query("SELECT id,last_name,first_name,password,access_id FROM nurse;")


        for row in database.execute_query("SELECT last_name FROM nurse;"):
            #personname = row[2] + " " + row[1]
            for last_name in row.keys():
                totalinfo = row[last_name]

        #_name = name
        return totalinfo
        #print("Hello, " + name)