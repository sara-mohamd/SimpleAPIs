from flask import Blueprint, request, jsonify
from app.models import User, db
from app.routes import protected_routes

authBluePrint = Blueprint("auth", __name__)


@authBluePrint.route('/user-details', methods=['GET'])
@protected_routes
def get_user_details(user):
    """
    Get User Details (Authenticated).

    This route returns the details of the authenticated user. The user must provide
    a valid token in the Authorization header to access this route.

    The response includes the user's ID, username, role, token, request count, and last request time.

    Returns:
        Response: A JSON response containing the user's details or an error message if not authenticated.
    """
    try:
        return jsonify(user.to_dict()), 200
    except Exception as e:
        return jsonify({"Error": str(e)}), 500
