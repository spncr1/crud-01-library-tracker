# CRUD routes for books
# Flask routes for our four main book management system functions:
# 1. GET /books, 2. POST /books, 3. PUT /books/<id>, 4. DELETE /books/<id>
from flask import Blueprint, jsonify, request
from models import db
from models.book import Book # importing the Book model and db session

# creating a Bluepritn for bookls
book_bp = Blueprint('book_bp', __name__)

# Route: GET /books
@book_bp.route('/books', methods=['GET'])
def get_books():
    """
    Fetch all books from the database and return as JSON.
    """
    books = Book.query.all() # get all bookl records
    # convert each Book object into a dictionary (K,V pairs)
    books_list = [ # using a list of dicts to store book information
        {
            "id" : book.id,
            "title" : book.title,
            "author" : book.author,
            "genre" : book.genre,
            "borrowed_status" : book.borrowed_status,
            "year" : book.year
        }
        for book in books
    ]
    return jsonify(books_list), 200 # HTTP code indicating that the client request has successfully been processed

# Route: POST /books
@book_bp.route('/books', methods=['POST'])
def add_book():
    """
    Add a new book to the database.
    Expects JSON body: {"id": "title", "author": "genre": "borrowed status": "year": (year i.e., 2024)}
    """
    data = request.get_json() # parse incoming JSON

    # Basic validation
    required_fields = ['title', 'author', 'genre', 'borrowed_status', 'year']
    if not data or not all (field in data for field in required_fields):
        return jsonify({"error" : "Missing required fields: title, author"}), 400

    new_book = Book(
        title=data['title'],
        author=data['author'],
        genre=data['genre'],
        borrowed_status=data['borrowed_status'],
        year=data.get('year')
    )

    # wrapping DB commits in a try-except block for robust error handling (will stay consistent with this for all other commits below)
    try:
        db.session.add(new_book)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Database error", "details": str(e)}), 500 # 500 = internal server error

    return jsonify({
        "id": new_book.id,
        "title": new_book.title,
        "author": new_book.author,
        "genre": new_book.genre,
        "borrowed_status": new_book.borrowed_status,
        "year": new_book.year
    }), 201 # 201 = HTTP code for "CREATED"

# Route: PUT /books/<id>
@book_bp.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    """
    Update an existing book in the database by its ID.
    Expects JSON body: {"title": "...", "author": "...", "genre": "...", "borrowed_status": ..., "year": ...}
    """

    data = request.get_json()

    # Fetch the book from the DB
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"error": f"Bookl with ID: {book_id} not found"}), 404 # returning HTTP code 404 to indicate an error occurred (unsucessful)

    # Update files if they exist in the incoming JSON
    book.title = data.get('title', book.title)
    book.author = data.get('author', book.author)
    book.genre = data.get('genre', book.genre)
    book.borrowed_status = data.get('borrowed_status', book.borrowed_status)
    book.year = data.get('year', book.year)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Database error", "details": str(e)}), 500

    return jsonify({
        "id": book.id,
        "title": book.title,
        "author": book.author,
        "genre": book.genre,
        "borrowed_status": book.borrowed_status,
        "year": book.year
    }), 200 # 200 = OK

# Route: DELETE /books/<id>
@book_bp.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    """
    Delete a book from the database using its ID.
    Simplest way to remove a book from the system is just entering its ID (better than having to type the title manually).
    """
    book = Book.query.get(book_id)

    if not book:
        return jsonify({"error": f"No book found with ID: {book_id}"}), 404

    try:
        db.session.delete(book)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Database error", "details": str(e)}), 500

    return jsonify({"message": f"Book with ID: {book_id} has been deleted from the Library Database."}), 200 # returns JSON