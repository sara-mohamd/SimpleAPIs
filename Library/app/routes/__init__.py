from flask import request, jsonify
from app.models import User

def protected_route():
    try:
        # Extract the token from the Authorization header
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        
        # Validate the token and retrieve the user
        user = User.query.filter_by(token=token).first()
        if not user:
            return jsonify({'message': 'Invalid token!'}), 401
        
        # If the token is valid, proceed with the main logic
        return jsonify({"message": f"Hello {user.username}, you have access to this route!"}), 201
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
