from app.DB import db
from app.models import Author
from flask import Blueprint, request, jsonify


"""
Author's routes

This module provides CRUD operations for the Author model.
It includes routes to create, retrieve, update, and delete authors.
"""

authorBluePrint = Blueprint('authors', __name__, url_prefix='/authors/')


@authorBluePrint.route('/', methods=['POST'])
def insertAuthor():
    """
    Create a new author.

    This route allows the creation of a new author. It expects a JSON payload
    with the 'name' field. The 'bio' field is optional. Only admins are allowed
    to access this route.

    Request JSON:
    {
        "name": "Author Name",
        "bio": "Author Biography"  # optional
    }

    Returns:
        JSON: The newly created author object.
        HTTP 201: If the author is created successfully.
        HTTP 400: If the request payload is invalid.
        HTTP 500: If there is a server error.
    """
    if not request.json or 'name' not in request.json:
        return jsonify({'error': 'Bad request'}), 400

    data = request.get_json()
    try:
        author = Author(data['name'], data.get('bio', ' '))
        db.session.add(author)
        db.session.commit()
        return jsonify(author.to_dict()), 201
    except Exception as e:
        db.session.rollback()    # ensures that partial changes are not saved
        return jsonify({"error": str(e)}), 500


@authorBluePrint.route('/<int:id>', methods=['GET'])
def getAuthor(id):
    """
    Retrieve details of a specific author by ID.

    This route allows retrieval of an author's details using their ID.

    Args:
        id (int): The ID of the author to retrieve.

    Returns:
        JSON: The author object if found.
        HTTP 200: If the author is found.
        HTTP 404: If the author does not exist.
        HTTP 500: If there is a server error.
    """
    try:
        author = Author.query.get(id)
        if author is None:
            return jsonify({'error': 'This author does not exist'}), 404
        return jsonify(author.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@authorBluePrint.route('/<int:id>', methods=['PUT'])
def updateEmp(id):
    """
    Update an author's biography.

    This route allows updating the biography of an existing author. Only admins
    are allowed to access this route.

    Args:
        id (int): The ID of the author to update.

    Request JSON:
    {
        "bio": "Updated Author Biography"
    }

    Returns:
        JSON: The updated author object.
        HTTP 200: If the update is successful.
        HTTP 400: If the request payload is invalid.
        HTTP 404: If the author does not exist.
        HTTP 500: If there is a server error.
    """
    if not request.json or 'bio' not in request.json:
        return jsonify({'error': 'Bad request'}), 400
    try:
        author = Author.query.get(id)
        if author is None:
            return jsonify({'error': 'Bad request'}), 400

        author.bio = request.json['bio']
        db.session.commit()
        return jsonify(author.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@authorBluePrint.route('/<int:id>', methods=['DELETE'])
def deleteAuthor(id):
    """
    Delete an author.

    This route allows deletion of an author by their ID.
    Only admins are allowed to access this route.

    Args:
        id (int): The ID of the author to delete.

    Returns:
        JSON: Success message if the author is deleted.
        HTTP 200: If the deletion is successful.
        HTTP 404: If the author does not exist.
        HTTP 500: If there is a server error.
    """
    try:
        author = Author.query.get(id)
        if author is None:
            return jsonify({'error': 'This author does not exist'}), 404

        db.session.delete(author)
        db.session.commit()
        return jsonify({"Sucess": "Author deleted!"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
