#!/usr/bin/env python3
"""
Main application for the API.
Sets up Flask app, routes, and error handling.
"""

from flask import Flask, jsonify, abort, request
from api.v1.auth.basic_auth import BasicAuth
from api.v1.auth.session_auth import SessionAuth
from api.v1.views import app_views
from flask_cors import CORS
from os import getenv

app = Flask(__name__)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

# Choose the authentication method based on AUTH_TYPE environment variable
auth = None
auth_type = getenv('AUTH_TYPE', 'basic_auth')
if auth_type == 'session_auth':
    auth = SessionAuth()
else:
    auth = BasicAuth()

@app.before_request
def before_request():
    """Ensure that the required authentication checks are performed."""
    excluded_paths = ['/api/v1/status/', '/api/v1/auth_session/login']
    if auth and not auth.require_auth(request.path, excluded_paths):
        return
    if (auth.authorization_header(request) is None and
            auth.session_cookie(request) is None):
        abort(401)

app.register_blueprint(app_views)

if __name__ == "__main__":
    app.run(host=getenv("API_HOST", "0.0.0.0"), port=int(getenv("API_PORT", "5000")))
