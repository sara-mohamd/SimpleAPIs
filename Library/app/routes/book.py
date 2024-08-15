"""
Book's routes

This module provides CRUD operations for the Book model.
It includes routes to create, retrieve, update, and delete books.
"""

from app.DB import db
from flask import Blueprint, request, jsonify
from app.models import Book, Author
from sqlalchemy.exc import IntegrityError
from routes import protected_route


"""
sqlalchemy.exc

module provides exception classes for handling errors
that occur during interactions with a database using SQLAlchemy.

IntegrityError:
    Purpose: Raised when an operation violates a database integrity constraint.
    This includes violations of unique constraints, foreign key constraints, and other constraints
    that ensure the accuracy and consistency of the data.


"""


bookBluePrint = Blueprint('book', __name__, url_prefix='/books')


@bookBluePrint.route('/', methods=['POST'])
def insertBook():
    """
    Create a new book.

    Expected JSON payload:
    {
        "title": "Book Title",
        "published_date": "YYYY-MM-DD",
        "isbn": "1234567890",
        "author_id": 1
    }

    Returns:
        JSON representation of the created book or an error message.
    """
    if not request.json or not all(k in request.json for k in ('title', 'published_date', 'isbn', 'author_id')):
        return jsonify({"Error": "Bad request"}), 400

    data = request.get_json()
    try:
        author_id = data['author_id']
        author = Author.query.get(author_id)
        if not author:
            return jsonify({"Error": "Author with given ID does not exist"}), 404
    except Exception as e:
        return jsonify({"Error": str(e)}), 500

    try:
        book = Book(data['title'], data['published_date'], data['isbn'], data['author_id'])
        db.session.add(book)
        db.session.commit()
        return jsonify(book.to_dict()), 201
    except IntegrityError as ie:
        db.session.rollback()
        if 'Duplicate entry' in str(ie):
            return jsonify({"Error": "ISBN already exists"}), 400
        return jsonify({"Error": str(ie)}), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({"Error": str(e)}), 500


@bookBluePrint.route('/<int:id>', methods=['GET'])
def getBook(id):
    """
    Retrieve details of a book by its ID.

    Args:
        id (int): Book ID.

    Returns:
        JSON representation of the book or an error message.
    """
    try:
        book = Book.query.get(id)
        if book is None:
            return jsonify({"Error": "This book does not exist"}), 404
        return jsonify(book.to_dict()), 200
    except Exception as e:
        return jsonify({"Error": str(e)}), 500


@bookBluePrint.route('/<int:id>', methods=['PUT'])
def updateBook(id):
    """
    Update book information by its ID.

    Expected JSON payload (partial updates allowed):
    {
        "title": "Updated Book Title"
    }

    Args:
        id (int): Book ID.

    Returns:
        JSON representation of the updated book or an error message.
    """
    if not request.json or "title" not in request.json:
        return jsonify({"Error": "Bad request"}), 400

    data = request.get_json()
    try:
        book = Book.query.get(id)
        if book is None:
            return jsonify({'Error': 'This book does not exist'}), 404

        if 'title' in data:
            book.title = data['title']
        db.session.commit()
        return jsonify(book.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"Error": str(e)}), 500


@bookBluePrint.route('/<int:id>', methods=['DELETE'])
def deleteBook(id):
    """
    Delete a book by its ID.

    Args:
        id (int): Book ID.

    Returns:
        Success message or an error message.
    """
    try:
        book = Book.query.get(id)
        if book is None:
            return jsonify({'Error': 'This book does not exist'}), 404

        db.session.delete(book)
        db.session.commit()
        return jsonify({"Success": "Book deleted!"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"Error": str(e)}), 500
