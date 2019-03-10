import sqlite3
import sys
from sqlite3 import Error
from faker import Faker
import app.classes.database_container
from app.common_definitions.common_paths import PATH_TO_DATABASE

import time
import glob


def create_connection(database_file_path):
    """
    Function takes 'database_file_path' (exact path of database in your directory or path + name of database you wish to create. Please write it down in main method)
    and creates database connecton to SQLite database specified inside the database_file_path. Returns connection object 'conn'
    """
    try:
        conn = sqlite3.connect(database_file_path)
        return conn
    except Error as e:
        print(e)

    return None


def create_in_memory_connection():
    """
    Function creates SQLite database in memory
    if you wish to use a temporary database, use this function but if you wish to empty previous database, 
    simply delete the db file containing the database you wish to empty.
    """
    try:
        conn = sqlite3.connect(':memory:')
        return conn
    except Error as e:
        print(e)

    return None


def create_table(database, sql_create_x_table):
    """
    Function takes database connection object 'conb' and sql statement to create table 'sql_create_x_table'.  
    creates table inside database. 
    """
    try:
        c = database.connection.cursor()
        c.execute(sql_create_x_table)
    except Error as e:
        print(e)


def close_connection(conn):
    """
    Function takes database connection object 'conn'.
    closes connection to database (good practice)
    """
    try:
        conn.close()
    except Error as e:
        print(e)


def initializeAndFillDatabase():
    """
    Main where we implement most methods above (create connection, create table, insert data, close connection.)
    """

    # Database already exists; do nothing
    if len(glob.glob(PATH_TO_DATABASE)) == 1:
        return False

    database = app.classes.database_container.DatabaseContainer.get_instance()

    app.classes.database_container.DatabaseContainer.commit_lock = True

    print("- Filling database -")

    # initialized variable with query that creates book table with columns/attributes
    table_creation_dict = {"patient_table": """CREATE TABLE IF NOT EXISTS patient (
                                                            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                                                            first_name TEXT NOT NULL,
                                                            last_name TEXT NOT NULL,
                                                            birthday  DATE NOT NULL,
                                                            gender    TEXT NOT NULL,
                                                            phone_number TEXT NOT NULL,
                                                            email  TEXT  NOT NULL ,
                                                            address TEXT NOT NULL , 
                                                            age  INTEGER NOT NULL,
                                                            health_card TEXT NOT NULL
                                                            
                                                        );""",

                           "doctor_table": """CREATE TABLE IF NOT EXISTS doctor (
                                        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                                        first_name TEXT NOT NULL,
                                        last_name TEXT NOT NULL,
                                        speciality  TEXT NOT NULL,
                                        city TEXT NOT NULL,
                                        password TEXT NOT NULL,
                                        permit_number integer NOT NULL 
                                        
                                    );""",

                           "room_table": """CREATE TABLE IF NOT EXISTS room (
                                        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                                        name TEXT NOT NULL  
                                    );""",

                           "appointment_table": """CREATE TABLE IF NOT EXISTS appointment (
                                        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                                        appointment_room  INTEGER NOT NULL,
                                        appointment_type TEXT NOT NULL,
                                        appointment_status TEXT NOT NULL,
                                        appointment_date DATE NOT NULL,
                                        start_time TIME NOT NULL,
                                        end_time TIME NOT NULL ,
                                        patient_id INTEGER NOT NULL,
                                        doctor_id INTEGER NOT NULL,
                                        
                                        FOREIGN KEY(appointment_room) REFERENCES room(id),
                                        FOREIGN KEY(patient_id) REFERENCES patient(id),
                                        FOREIGN KEY(doctor_id) REFERENCES doctor(id)  
                                    );""",
                           "doctoravailablility_table": """CREATE TABLE IF NOT EXISTS doctoravailability  (
                                        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                                        date_day TEXT NOT NULL,
                                        start_time TIME NOT NULL,
                                        end_time TIME NOT NULL ,
                                        doctor_id INTEGER NOT NULL,
                                        FOREIGN KEY(doctor_id) REFERENCES doctor(id)
                                    );""",
                           "nurse_table": """CREATE TABLE IF NOT EXISTS nurse  (
                                            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                                            last_name TEXT NOT NULL,
                                            first_name TEXT NOT NULL,
                                            password TEXT NOT NULL, 
                                            access_id TEXT NOT NULL
                                            
                                            
                                        );""",


                           }

    # Create all tables
    for table_name, table_sql in table_creation_dict.items():
        database.execute_query(table_sql)

    app.classes.database_container.DatabaseContainer.commit_lock = False
    database.commit_db()

    #

    # Don't commit until the end
    app.classes.database_container.DatabaseContainer.commit_lock = True

    print("- Finished filling database -")

    # Turn off commit lock
    app.classes.database_container.DatabaseContainer.commit_lock = False
    database.commit_db()

    return True
