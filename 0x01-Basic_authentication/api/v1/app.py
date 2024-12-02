#!/usr/bin/env python3
"""
Route module for the API.
Handles application initialization, error handling, and authentication setup.
"""

from flask import Flask, jsonify
from flask_cors import CORS
from api.v1.views import app_views
from os import getenv
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth

# Initialize Flask application
app = Flask(__name__)

# Register Blueprint for views
app.register_blueprint(app_views)

# Enable Cross-Origin Resource Sharing (CORS)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

# Authentication setup
auth = None
auth_type = getenv('AUTH_TYPE', 'auth')
if auth_type == 'basic_auth':
    auth = BasicAuth()
else:
    auth = Auth()


@app.errorhandler(401)
def unauthorized_error(error):
    """
    Error handler for unauthorized access (401).
    Returns:
        JSON response with error message and status code 401.
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden_error(error):
    """
    Error handler for forbidden access (403).
    Returns:
        JSON response with error message and status code 403.
    """
    return jsonify({"error": "Forbidden"}), 403


@app.errorhandler(404)
def not_found(error):
    """
    Error handler for resource not found (404).
    Returns:
        JSON response with error message and status code 404.
    """
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    """
    Main entry point of the API server.
    Reads API_HOST and API_PORT environment variables to start the server.
    Defaults to 0.0.0.0 and port 5000 if variables are not set.
    """
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=int(port), threaded=True)
