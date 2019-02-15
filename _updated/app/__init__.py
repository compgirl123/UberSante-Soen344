import os
import sys
from flask import Flask

app = Flask(__name__)

from  models import DatabaseContainer
from  common_definitions.common_paths import PATH_TO_DATABASE
from database import sqlite_script


# Create and fill database with values - closes connection to
# Database was filled, objects are in memory if function call returns True
objects_in_memory = sqlite_script.initializeAndFillDatabase()


# Connect to the database through an abstracted object - this object must be imported into route files for use
databaseObject = DatabaseContainer.get_instance()




