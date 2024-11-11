#!/usr/bin/env python3
"""
This module defines the Blueprint 'app_views' for handling API views.
It includes a route for checking the API status.
"""

from flask import Blueprint, jsonify

app_views = Blueprint('app_views', __name__)

@app_views.route('/status', methods=['GET'])
def status():
    """
    Return the status of the API.
    
    Returns:
        dict: JSON response with the API status.
    """
    return jsonify({"status": "OK"})
