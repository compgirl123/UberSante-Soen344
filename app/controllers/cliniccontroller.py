import sqlite3
import sqlite3 as mysql
import sqlite3 as sql
import sys
import shutil
from sqlite3 import Error
import app.classes.database_container
from app.common_definitions.common_paths import PATH_TO_DATABASE
#from app.controllers.cliniccontroller import *
from app.classes.database_container import DatabaseContainer as db


class Cliniccontroller:

    def get_all_clinics(self):

        '''
        Creating Arrays to Store the values of each column for the Clinic Table
        '''
        clinic_names = []
        clinic_locations = []

        table_creation_dict = {"clinic": "SELECT name,location FROM clinic;"}
        database = app.classes.database_container.DatabaseContainer.get_instance()

        for table_name, table_sql in table_creation_dict.items():
            database.execute_query(table_sql)

        results = database.execute_query("SELECT name,location FROM clinic;")

        for row in database.execute_query("SELECT DISTINCT name,location FROM clinic;"):
            clinic_names.append(row["name"])
            clinic_locations.append(row["location"])
            

        values_from_db = tuple(list(zip(clinic_names,clinic_locations)))
        return values_from_db

    