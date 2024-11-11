#!/usr/bin/env python3
""" Authentication template class for the API. """
from flask import request
from typing import List
from typing import List, TypeVar


class Auth:
    """ Base authentication class with utility methods. """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Check if path requires authentication. """
        return False


    def authorization_header(self, request=None) -> str:
        """ Retrieve the Authorization header from the request. """
        if request is None or 'Authorization' not in request.headers:
            return None
        return request.headers['Authorization']


    def current_user(self, request=None) -> TypeVar('User'):
        """ Retrieve the current user from the request. """
        return None


    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Determine if a path requires authentication. """
        if path is None:
            return True
        if excluded_paths is None or not excluded_paths:
            return True
        if path[-1] != '/':
            path += '/'
        return path not in excluded_paths

     def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Returns True if authentication is required for the given path.
        Returns False if the path is in the excluded_paths list (with support for wildcard `*` at the end of paths).
        """
        for excluded_path in excluded_paths:
            if excluded_path.endswith("*"):
                """ Check if the path starts with the excluded_path without the '*' """
                if path.startswith(excluded_path[:-1]):
                    return False
            elif path == excluded_path:
                return False
        return True
