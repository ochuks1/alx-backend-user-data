#!/usr/bin/env python3
"""
Session Authentication class for API access.
Provides methods to manage user sessions.
"""

from api.v1.auth.auth import Auth
from typing import Dict, TypeVar
import uuid
from os import getenv


class SessionAuth(Auth):
    """ Session authentication implementation (inherits from Auth). """

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Create a Session ID for a user_id.

        Args:
            user_id (str): The ID of the user.

        Returns:
            str: The Session ID or None if invalid.
        """
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Return a User ID based on a Session ID.

        Args:
            session_id (str): The Session ID.

        Returns:
            str: The User ID associated with the Session ID or None if invalid.
        """
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieve the current User based on a Session ID from a cookie.

        Args:
            request: The Flask request object.

        Returns:
            User: The authenticated User object or None if authentication fails.
        """
        session_id = self.session_cookie(request)
        if session_id is None:
            return None
        user_id = self.user_id_for_session_id(session_id)
        return User.get(user_id) if user_id else None

    def session_cookie(self, request=None) -> str:
        """
        Return the session cookie value from a request.

        Args:
            request: The Flask request object.

        Returns:
            str: The session cookie value or None if not present.
        """
        if request is None:
            return None
        session_name = getenv('SESSION_NAME', '_my_session_id')
        return request.cookies.get(session_name)
