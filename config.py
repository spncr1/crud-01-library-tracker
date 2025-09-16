# Configuration of project to control settings and behaviour of the project overall in one centralised module
# Goal of this module is to let the app load the DB URI so that the books.db file lives in the 'instance' folder and is not committed to git

import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    DEBUG = False
    TESTING = False

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///" + os.path.join(BASE_DIR, "instance", "books.db"))

    # Avoid SQLAlchemy warning and extra overhead
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True