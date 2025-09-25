# Configuration of project to control settings and behaviour of the project overall in one centralised module
# Goal of this module is to let the app load the DB URI so that the books.db file lives in the 'instance' folder and is not committed to git

import os

class Config:
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False # Avoid SQLAlchemy warning and extra overhead

class DevelopmentConfig(Config):
    DEBUG = True
    # SQLite DB will live inside Flask's instance folder, relative to app root
    SQLALCHEMY_DATABASE_URI = None # we don't need to set this here, will be set dynamically in create_app() from app.py