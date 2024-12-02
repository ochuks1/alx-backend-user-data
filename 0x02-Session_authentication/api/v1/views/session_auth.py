#!/usr/bin/env python3
"""
Views for handling Session Authentication endpoints.
"""

from flask import jsonify, abort, request
from api.v1.views import app_views
from api.v1.auth.session_auth import SessionAuth
from models.user import User

auth = SessionAuth()

@app_views.route('/api/v1/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """Handle user login and create session."""
    email = request.json.get('email')
    password = request.json.get('password')

    # Check for missing parameters
    if email is None and password is None:
        return jsonify({"error": "Missing email and password"}), 400
    if email is None:
        return jsonify({"error": "Missing email"}), 400
    if password is None:
        return jsonify({"error": "Missing password"}), 400

    # Authenticate user
    user = User.search({'email': email})
    if not user:
        return jsonify({"error": "Wrong email"}), 401

    user = user[0]
    if not user.is_valid_password(password):
        return jsonify({"error": "Wrong password"}), 401

    # Create session
    session_id = auth.create_session(user.id)
    response = jsonify(user.to_dict())
    response.set_cookie(getenv('SESSION_NAME', '_my_session_id'), session_id)
    return response
