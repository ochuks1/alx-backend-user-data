#!/usr/bin/env python3
"""
Basic Authentication class for API access.
Implements methods for handling Basic Auth logic.
"""

import base64
from api.v1.auth.auth import Auth
from models.user import User
from typing import Tuple, TypeVar


class BasicAuth(Auth):
    """ Basic authentication implementation (inherits from Auth). """

    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """
        Extract the Base64 authorization part from the header.

        Args:
            authorization_header (str): The full Authorization header.

        Returns:
            str: The Base64 encoded part of the header, or None if invalid.
        """
        if authorization_header is None or not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header.split(" ")[1]

    def decode_base64_authorization_header(self, base64_authorization_header: str) -> str:
        """
        Decode the Base64 authorization header.

        Args:
            base64_authorization_header (str): The Base64 encoded string.

        Returns:
            str: The decoded string, or None if decoding fails.
        """
        if base64_authorization_header is None or not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded = base64.b64decode(base64_authorization_header).decode('utf-8')
            return decoded
        except Exception:
            return None

    def extract_user_credentials(self, decoded_base64_authorization_header: str) -> Tuple[str, str]:
        """
        Extract user credentials (email and password) from the decoded header.

        Args:
            decoded_base64_authorization_header (str): The decoded string.

        Returns:
            Tuple[str, str]: A tuple containing (email, password) or (None, None) if invalid.
        """
        if decoded_base64_authorization_header is None or not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        return tuple(decoded_base64_authorization_header.split(":", 1))

    def user_object_from_credentials(self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """
        Retrieve the User object based on the provided email and password.

        Args:
            user_email (str): The user's email.
            user_pwd (str): The user's password.

        Returns:
            User: The User object if credentials are valid, otherwise None.
        """
        if not isinstance(user_email, str) or not isinstance(user_pwd, str):
            return None
        try:
            users = User.search({'email': user_email})
            if not users or not users[0].is_valid_password(user_pwd):
                return None
            return users[0]
        except Exception:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieve the current User object based on the Authorization header.

        Args:
            request: The Flask request object.

        Returns:
            User: The authenticated User object, or None if authentication fails.
        """
        authorization_header = self.authorization_header(request)
        if authorization_header is None:
            return None
        base64_header = self.extract_base64_authorization_header(authorization_header)
        if base64_header is None:
            return None
        decoded_header = self.decode_base64_authorization_header(base64_header)
        if decoded_header is None:
            return None
        user_email, user_pwd = self.extract_user_credentials(decoded_header)
        if user_email is None or user_pwd is None:
            return None
        return self.user_object_from_credentials(user_email, user_pwd)
