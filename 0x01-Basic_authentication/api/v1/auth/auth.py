#!/usr/bin/env python3
"""
Authentication template class for the API.
Provides base methods for authorization and user validation.
"""

from flask import request
from typing import List, TypeVar


class Auth:
    """ Base authentication class with utility methods. """

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

        # Check if the path matches any excluded path (supports wildcard *)
        for excluded_path in excluded_paths:
            if excluded_path.endswith("*") and path.startswith(excluded_path[:-1]):
                return False
            elif path == excluded_path:
                return False

        return True

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
            TypeVar('User'): Always returns None in this base class.
        """
        return None
