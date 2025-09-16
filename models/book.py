# Book model & details (i.e., id, title, author, genre, year, status (currently borrowed, previously borrowed, in-store, online etc.)
from app import db # importing SQLAlchemy instance from app.py

class Book (db.Model):
    """
    This class defines the 'books' table in the DB, where:
    Each attribute becomes a column in the table
    """
    __tablename__ = 'books' # name of our SQL table

    id = db.Column(db.Integer, primary_key=True) # unique identifier for each book
    title = db.Column(db.String(150), nullable=False) # text required i.e., cannot be null
    author = db.Column(db.String(150), nullable=False) # text required i.e., cannot be null
    genre = db.Column(db.String(150), nullable=False) # text required i.e., cannot be null
    borrowed_status = db.Column(db.String(150), nullable=False) # returns true if the book has been borrowed, false by default i.e., all books in the library DB are currently stored in the library to start

    def __repr__ (self): # __repr__ = special dunder method that tells the interpreter how to represent an object as a string - automatically called in the right contexts
        return f"<Book {self.id}: {self.title} by {self.author}" # this is how I want the object (book) to be displayed