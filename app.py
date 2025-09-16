# Entry point: used to run the Flask app
# NOTES #
# use 'flask run' to run the project and make changes for different iterations
# try not to use python app.py to run the project
# use control C to quit the currently running server
import os
from flask import Flask # micro web framework
from flask_sqlalchemy import SQLAlchemy # Flask extension for DB ORM
from config import DevelopmentConfig # settings modeule (DB URI, debug mode)

db = SQLAlchemy() # initialise SQLAlchemy isntance globally (binded into the app later)

"""
app factory - creates and configures Flask app instance each time the server is run
helps with:
- testing (multiple instances)
- blueprints
- extensions i.e., SQLAlchemy 
"""
def create_app():
    app = Flask(__name__, instance_relative_config=True)     # Create Flask app
    app.config.from_object(DevelopmentConfig) # load settings from our DevelopmentConfig (DB URI, debug mode) defined in config.py
    db.init_app(app) # bind SQLAlchemy to this app instance, facilitating models (books) interaction with DB
    os.makedirs(app.instance_path, exist_ok=True) # ensure the 'instance' folder exists for SQLite DB

    @app.route('/')
    def home():
        return "Hello, World!" # Flask takes this return string and sends it as HTML to the browser

    # Return the app so it can be run by the command line or other scripts
    return app

# Only run this block if app.py is executed directly (not imported)
if __name__ == "__main__":
    create_app().run(debug=True)