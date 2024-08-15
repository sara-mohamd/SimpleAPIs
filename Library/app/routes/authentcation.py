from flask import Blueprint, request, jsonify
from app.models import User, db
from routes import protected_route


authBluePrint = Blueprint("auth", __name__)

@authBluePrint.route('/register', methods=['POST'])
def register():
    
    try:
        data = request.get_json()
    except Exception as e:
        ...


@authBluePrint.route('/login', methods=['POST'])
def login():
    """
    Handles user login by validating the provided username and password.

    - Checks if the username and password are provided in the request body.
    - Verifies if the user exists and if the password matches.
    - If successful, generates a unique token for the user and updates their token in the database.
    - Returns the token in the response if login is successful.
    - Returns error messages if login fails.

    Request Body (JSON):
    {
        "username": "string",
        "password": "string"
    }

    Returns:
        - 200: If login is successful, returns a JSON with a message and the user's token.
        - 400: If username or password is missing from the request body.
        - 401: If the user doesn't exist or the password is incorrect.
    """
    try:
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return jsonify({"Error": "Check username or password"}), 400

        # Query the database for the user by username
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            user.token = User.generate_token()
            db.session.commit()
            return jsonify({"message": f"Login successful Token : {user.token}" }), 200
        else:
            return jsonify({"Message": "Invalid username or password"}), 401

    except Exception as e:
        return jsonify({"error": str(e)}), 500


