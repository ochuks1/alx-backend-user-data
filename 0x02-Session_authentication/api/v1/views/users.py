#!/usr/bin/env python3
"""
Views for handling User endpoints.
"""

from flask import jsonify, abort, request
from api.v1.views import app_views
from models.user import User

@app_views.route('/api/v1/users/me', methods=['GET'], strict_slashes=False)
def get_me():
    """Retrieve the current User."""
    if request.current_user is None:
        abort(404)
    return jsonify(request.current_user.to_dict()), 200

@app_views.route('/api/v1/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """Retrieve a User by user_id."""
    if user_id == "me":
        if request.current_user is None:
            abort(404)
        return jsonify(request.current_user.to_dict()), 200
    user = User.get(user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict()), 200
