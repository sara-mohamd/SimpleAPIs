from flask import request, jsonify
from app.models import User
from functools import wraps
"""

- To be used as a decorator: @protected_routes
- Flask decorators like @protected_routes
need to be written in a way that allows them to wrap around view functions.

"""


def protected_routes(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        try:
            # Extract the token from the Authorization header
            token = request.headers.get('Authorization')
            
            if not token:
                return jsonify({'message': 'Token is missing!'}), 401
            
            # Validate the token and retrieve the user
            user = User.query.filter_by(token=token).first()
            if not user:
                return jsonify({'message': 'Invalid token!'}), 401
            
            # Pass the user to the view function
            return func(user, *args, **kwargs)
        
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return decorated_function


def is_admin(user):
        """
        Checks if the user has an admin role.
        """
        return user.role.lower() == "admin"