# one-off script to create tables for our DB
# creates the SQLite DB file and tables (based on SQLAlchemy models)
import os
from app import create_app, db # import app factory and SQLAlchemy isntance
from models.book import Book # import models from book module so SQLAlchemy can see them

app = create_app() # create app instance

with app.app_context(): # use app context to run DB commands
    db.create_all() # this creates all tables defined for models in the DB
    db_path = os.path.join(app.instance_path, "books.db")
    print("Database and tables created successfully!")
    print(f"Database created at: {db_path}")