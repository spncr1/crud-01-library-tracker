# Entry point: used to run the Flask app
# NOTES #
# use 'flask run' to run the project and make changes for different iterations
# try not to use python app.py to run the project
# use control C to quit the currently running server
import os
from flask import Flask, jsonify, redirect, url_for # micro web framework
from flask_sqlalchemy import SQLAlchemy # Flask extension for DB ORM
from config import DevelopmentConfig # settings modeule (DB URI, debug mode)
from routes.book_routes import book_bp
from models import db

"""
app factory - creates and configures Flask app instance each time the server is run
helps with:
- testing (multiple instances)
- blueprints
- extensions i.e., SQLAlchemy 
"""

def create_app():
    app = Flask(__name__, instance_relative_config=True)     # Create Flask app
    os.makedirs(app.instance_path, exist_ok=True) # ensure the 'instance' folder exists for SQLite DB

    # load settings from our DevelopmentConfig (DB URI, debug mode) defined in config.py
    app.config.from_object(DevelopmentConfig)

    db_path = os.path.join(app.instance_path, "books.db")
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"

    db.init_app(app) # bind SQLAlchemy to this app instance, facilitating models (books) interaction with DB - MUST be called before registering the routes (below)

    # Register the blueprint
    app.register_blueprint(book_bp, url_prefix='/books')

    # Basic HTTP error code handling
    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({"error": "Resource not found"}), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({"error": "Internal server error"}), 500

    @app.route('/')
    def home():
        return redirect(url_for('book_bp.get_books')) # Flask takes this return string and sends it as HTML to the browser

    # Return the app so it can be run by the command line or other scripts
    return app

# Only run this block if app.py is executed directly (not imported)
if __name__ == "__main__":
    create_app().run(debug=True)