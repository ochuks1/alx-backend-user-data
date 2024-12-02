#!/usr/bin/env python3
"""
Views module for the API.
Defines the app_views blueprint and imports views.
"""

from flask import Blueprint

app_views = Blueprint('app_views', __name__)

# Import views
from api.v1.views.users import *
from api.v1.views.session_auth import *  # Add this line
