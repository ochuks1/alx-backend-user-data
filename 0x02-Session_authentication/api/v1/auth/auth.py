#!/usr/bin/env python3
"""
Authentication base class for the API.
Provides utility methods for authentication processes.
"""

from flask import request
from typing import List, TypeVar


class Auth:
    """ Base class for API authentication. """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determine if a path requires authentication.

        Args:
            path (str): The path to check.
            excluded_paths (List[str]): A list of paths that do not require authentication.

        Returns:
            bool: True if the path requires authentication, False otherwise.
        """
        if path is None or excluded_paths is None or not excluded_paths:
            return True

        # Normalize the path to ensure trailing slash consistency
        if path[-1] != '/':
            path += '/'

        return path not in excluded_paths

    def authorization_header(self, request=None) -> str:
        """
        Retrieve the Authorization header from the request.

        Args:
            request: The Flask request object.

        Returns:
            str: The value of the Authorization header, or None if not present.
        """
        if request is None or 'Authorization' not in request.headers:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieve the current user from the request.

        Args:
            request: The Flask request object.

        Returns:
            User: Always returns None in this base class.
        """
        return None
