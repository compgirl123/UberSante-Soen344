import logging

from flask import Flask, request as req

from app.controllers import pages

from app.classes.database_container import DatabaseContainer
from app.common_definitions.common_paths import PATH_TO_DATABASE
from app.database import sqlite_script

# Create and fill database with values - closes connection to
# Database was filled, objects are in memory if function call returns True
objects_in_memory = sqlite_script.initializeAndFillDatabase()


# Connect to the database through an abstracted object - this object must be imported into route files for use
databaseObject = DatabaseContainer.get_instance()


def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_object(config_filename)

    app.register_blueprint(pages.blueprint)

    app.logger.setLevel(logging.NOTSET)

    @app.after_request
    def log_response(resp):
        app.logger.info("{} {} {}\n{}".format(
            req.method, req.url, req.data, resp)
        )
        return resp

    return app
