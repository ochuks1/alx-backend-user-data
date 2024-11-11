#!/usr/bin/env python3
""" Basic Authentication class for API access. """
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """ Basic authentication implementation (inherits from Auth). """
    pass


"""BasicAuth class for Basic Authentication"""

import base64
from models.user import User


class BasicAuth(Auth):
    """Basic Authentication class"""

    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """Extract Base64 authorization part from header"""
        if authorization_header is None or not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header.split(" ")[1]


     def decode_base64_authorization_header(self, base64_authorization_header: str) -> str:
        if base64_authorization_header is None or not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded = base64.b64decode(base64_authorization_header).decode('utf-8')
            return decoded
        except Exception:
            return None


    def extract_user_credentials(self, decoded_base64_authorization_header: str) -> (str, str):
        if decoded_base64_authorization_header is None or not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        return decoded_base64_authorization_header.split(":", 1)


    def user_object_from_credentials(self, user_email: str, user_pwd: str) -> 'User':
        if not isinstance(user_email, str) or not isinstance(user_pwd, str):
            return None
        try:
            user = User.search({'email': user_email})
            if not user or not user[0].is_valid_password(user_pwd):
                return None
            return user[0]
        except Exception:
            return None


    def current_user(self, request=None) -> 'User':
        """Retrieve the current user for a request"""
        authorization_header = request.headers.get('Authorization')
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
