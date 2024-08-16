"""
BorrowRecord's routes

This module provides CRUD operations for the BorrowRecord model.
It includes routes to create, retrieve, update, and delete borrow records.
"""

from app.DB import db
from flask import Blueprint, request, jsonify
from datetime import datetime
from sqlalchemy.exc import IntegrityError, DataError
from app.models import BorrowRecord
from app.routes import protected_routes

borrowBluePrint = Blueprint('borrow_record', __name__, url_prefix='/borrowRecords/')


@borrowBluePrint.route('/', methods=['POST'])
@protected_routes
def insertBorrowRecord():
    """
    Create a new borrow record.

    This route allows the creation of a new borrow record. It expects a JSON payload
    with 'borrow_date', 'book_id', 'user_id', and optionally 'return_date'.

    Request JSON:
    {
        "borrow_date": "YYYY-MM-DD",
        "book_id": 1,
        "user_id": 1,
        "return_date": "YYYY-MM-DD"  # optional
    }

    Returns:
        JSON: The newly created borrow record object.
        HTTP 201: If the borrow record is created successfully.
        HTTP 400: If the request payload is invalid or has incorrect data format.
        HTTP 404: If the foreign keys do not reference existing records.
        HTTP 500: If there is a server error.
    """
    if not request.json or not all(k in request.json for k in ('borrow_date', 'book_id', 'user_id')):
        return jsonify({"Error": "Bad request"}), 400

    data = request.get_json()
    try:
        borrow_date = datetime.strptime(data['borrow_date'], '%Y-%m-%d').date()
        return_date = datetime.strptime(data['return_date'], '%Y-%m-%d').date() if 'return_date' in data else None
    except ValueError:
        return jsonify({"Error": "Invalid date format. Expected YYYY-MM-DD"}), 400

    try:
        borrow = BorrowRecord(borrow_date=borrow_date, book_id=data['book_id'], user_id=data['user_id'], return_date=return_date)
        db.session.add(borrow)
        db.session.commit()
        return jsonify(borrow.to_dict()), 201
    except IntegrityError as ei:
        db.session.rollback()
        return jsonify({"Error": f"Integrity error\n{str(ei.orig)}"}), 404
    except DataError as e:
        db.session.rollback()
        return jsonify({"Error": f"Data Error: {str(e.orig)}"}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"Error": str(e)}), 500


@borrowBluePrint.route('/<int:id>', methods=['GET'])
def getBorrowRecord(id):
    """
    Retrieve details of a Borrow Record by its ID.

    Args:
        id (int): Borrow record ID.

    Returns:
        JSON representation of the borrow record or an error message.
    """
    try:
        borrow = BorrowRecord.query.get(id)
        if borrow is None:
            return jsonify({"Error": "This BorrowRecord does not exist"}), 404
        return jsonify(borrow.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"Error": str(e)}), 500


@borrowBluePrint.route('/<int:id>', methods=['PUT'])
@protected_routes
def updateBorrowRecord(id):
    """
    Update a borrow record by its ID.

    Args:
        id (int): Borrow record ID.

    Request JSON:
    {
        "return_date": "YYYY-MM-DD",  # optional
        "book_id": 1,  # optional
        "user_id": 1   # optional
    }

    Returns:
        JSON: The updated borrow record object.
        HTTP 200: If the update is successful.
        HTTP 400: If the request payload is invalid or has incorrect data format.
        HTTP 404: If the borrow record does not exist.
        HTTP 500: If there is a server error.
    """
    if not request.json:
        return jsonify({"Error": "Bad request"}), 400

    data = request.get_json()
    try:
        borrow = BorrowRecord.query.get(id)
        if borrow is None:
            return jsonify({'Error': 'This BorrowRecord does not exist'}), 404

        if 'return_date' in data:
            try:
                borrow.return_date = datetime.strptime(data['return_date'], '%Y-%m-%d').date()
            except ValueError:
                return jsonify({"Error": "Invalid date format. Expected YYYY-MM-DD"}), 400
        if 'book_id' in data:
            borrow.book_id = data['book_id']
        if 'user_id' in data:
            borrow.user_id = data['user_id']

        db.session.commit()
        return jsonify(borrow.to_dict()), 200
    except IntegrityError as ei:
        db.session.rollback()
        return jsonify({"Error": f"Integrity error\n{str(ei.orig)}"}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({"Error": str(e)}), 500


@borrowBluePrint.route('/<int:id>', methods=['DELETE'])
@protected_routes
def deleteBorrowRecord(id):
    """
    Delete a Borrow Record by its ID.

    Args:
        id (int): Borrow record ID.

    Returns:
        Success message or an error message.
    """
    try:
        borrow = BorrowRecord.query.get(id)
        if borrow is None:
            return jsonify({'Error': 'This BorrowRecord does not exist'}), 404
        db.session.delete(borrow)
        db.session.commit()
        return jsonify({"Success": "Borrow Record deleted!"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"Error": str(e)}), 500
