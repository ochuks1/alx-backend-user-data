#!/usr/bin/env python3
"""
Module of Index views for Flask API.
Defines routes to provide API status, statistics, and error handling.
"""

from flask import Flask, Blueprint, jsonify, abort
from api.v1.views import app_views

app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status() -> str:
    """
    GET /api/v1/status
    Returns:
        JSON response with the status of the API.
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats() -> str:
    """
    GET /api/v1/stats
    Returns:
        JSON response with the count of each object type.
    """
    from models.user import User
    stats = {
        "users": User.count()
    }
    return jsonify(stats)


@app_views.route('/unauthorized', methods=['GET'], strict_slashes=False)
def unauthorized_route():
    """
    GET /api/v1/unauthorized
    Purpose:
        Route to raise a 401 Unauthorized error.
    Returns:
        Aborts the request with a 401 status code.
    """
    abort(401)


@app_views.route('/forbidden', methods=['GET'], strict_slashes=False)
def forbidden_route():
    """
    GET /api/v1/forbidden
    Purpose:
        Route to raise a 403 Forbidden error.
    Returns:
        Aborts the request with a 403 status code.
    """
    abort(403)


# Custom error handlers for unauthorized and forbidden routes
@app_views.errorhandler(401)
def unauthorized_error(error):
    """
    Custom error handler for 401 Unauthorized.
    Returns:
        JSON response with error message and status code 401.
    """
    return jsonify({"error": "Unauthorized"}), 401


@app_views.errorhandler(403)
def forbidden_error(error):
    """
    Custom error handler for 403 Forbidden.
    Returns:
        JSON response with error message and status code 403.
    """
    return jsonify({"error": "Forbidden"}), 403
