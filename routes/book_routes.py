# CRUD routes for books
# Flask routes for our four main book management system functions:
# 1. GET /books, 2. POST /books, 3. PUT /books/<id>, 4. DELETE /books/<id>
# ------------------------------
# PROJECT UPDATE: for Day 3, we are integrating the backend with HTML templates using Jinja2, instead of returning JSON.
# This allows the frontend MVP to display books in a table, and handle user form submissions directly via the browser.
# JSON endpoints are still useful for future API use, but for the MVP UI, render_templates is needed as a replacement
# ------------------------------
from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db
from models.book import Book # importing the Book model and db session

# creating a Bluepritn for bookls
book_bp = Blueprint('book_bp', __name__)

# Route: GET /books
@book_bp.route('/', methods=['GET'])
def get_books():
    """
    Fetch all books from the database and render the HTML table.
    Replaces the previous JSON response (placeholder logic) with Jinja2 template rendering, as part of Day 3's tasks.
    Now supports optional search query via ?query= as well.
    """
    search_query = request.args.get("query", "").strip()

    if search_query:
        # Filter by title or author (case-insensitive)
        books = Book.query.filter(
            (Book.title.ilike(f"%{search_query}")) |
            (Book.author.ilike(f"{search_query}"))
        ).all()
    else:
        books = Book.query.all()
    # Pass the book objects directly to index.html
    # Jinja2 can access attributes like book.title, book.author, etc.
    return render_template("index.html", books=books, search_query=search_query)

# GET Add Book Page
@book_bp.route('/add', methods=['GET'])
def add_book_page():
    return render_template('add_book.html')

# POST Add Book
@book_bp.route('/', methods=['POST'])
def add_book():
    """
    Add a new book to the database via form submission.
    Expects form data: title, author, genre, borrowed_status, year
    Redirects back to /books to refresh the list and show the newly added book/s.
    """

    # Retrieve form data from the HTML form (not JSON anymore)
    title = request.form.get('title', '').strip()
    author = request.form.get('author', '').strip()
    genre = request.form.get('genre')
    borrowed_status = request.form.get('borrowed_status')
    year = request.form.get('year')

    # Basic input validation so user knows why their submission failed
    if not title or not author:
        # If missing required fields, redirect back (will implement flash message later)
        flash("Both Title and Author are requried!", "error")
        return redirect(url_for('book_bp.get_books'))

    # Create new Book instance
    new_book = Book(
        title=title,
        author=author,
        genre=genre,
        borrowed_status=borrowed_status,
        year=year
    )

    # save to DB - using try-except block for robust error handling in case something goes wrong
    try:
        db.session.add(new_book)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        # For MVP, we redirect; in production, an error page may be displayed
        return redirect(url_for('book_bp.get_books'))

    # Redirect to /books to show updated list (full page reload)
    return redirect(url_for('book_bp.get_books'))

# GET Edit Book Page
@book_bp.route('/<int:book_id>/edit', methods=['GET'])
def edit_book(book_id):
    """
    Render the edit form for a specific book.
    Fetches the current book data and passes it to the template.
    """
    book = Book.query.get_or_404(book_id) # fetch book or 404 if not found
    return render_template("edit_book.html", book=book)

# POST Update Book
@book_bp.route('/<int:book_id>/update', methods=['POST'])
def update_book(book_id):
    """
    Process the form submission and update the book in the DB.
    NOTE: HTML forms do not support PUT natively, so we use POST instead of PUT here for simplicity.
    Expects form fields same as add_book.
    """

    # Fetch the book from the DB
    book = Book.query.get_or_404(book_id) # Fetch book or 404 if not found

    # Update fields if they exist in the form submission
    title = request.form.get('title', '').strip()
    author = request.form.get('author', '').strip()
    book.genre = request.form.get('genre', book.genre)
    book.borrowed_status = request.form.get('borrowed_status', book.borrowed_status)
    book.year = request.form.get('year', book.year)

    if not title or not author:
        flash("Both Title and Author are required!", "error")
        return redirect(url_for('book_bp.edit_book', book_id=book.id))

    book.title = title
    book.author = author

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        flash(f"Error updating book: {e}")

    return redirect(url_for('book_bp.get_books'))

# GET Delete Book Page
@book_bp.route('/delete', methods=['GET'])
def delete_book_page():
    books = Book.query.all()
    return render_template('delete_book.html', books=books)

# POST Delete Book
@book_bp.route('/<int:book_id>/delete', methods=['POST'])
def delete_book(book_id):
    """
    Delete a book from the database using a form submission or delete button (can implement later).
    NOTE: HTML forms do not suppoort DELETE natively, so we use POST here instead.
    """
    book = Book.query.get(book_id)
    if not book:
        return redirect(url_for('book_bp.get_books'))

    try:
        db.session.delete(book)
        db.session.commit()
    except Exception as e:
        db.session.rollback()

    return redirect(url_for('book_bp.get_books'))