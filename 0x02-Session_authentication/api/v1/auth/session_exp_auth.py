#!/usr/bin/env python3
""" SessionExpAuth class for handling session authentication with expiration. """

from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
from os import getenv


class SessionExpAuth(SessionAuth):
    """ Session authentication class with expiration feature. """

    def __init__(self):
        """ Initializes the session expiration duration. """
        super().__init__()
        try:
            self.session_duration = int(getenv("SESSION_DURATION", 0))
        except ValueError:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """ Creates a session ID with expiration. """
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        
        # Store session data with user ID and created time
        self.user_id_by_session_id[session_id] = {
            "user_id": user_id,
            "created_at": datetime.now()
        }
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ Retrieves user ID based on session ID, considering expiration. """
        if session_id is None:
            return None
        session_data = self.user_id_by_session_id.get(session_id)
        if session_data is None:
            return None

        if self.session_duration <= 0:
            return session_data["user_id"]

        created_at = session_data.get("created_at")
        if created_at is None:
            return None
        
        # Check if the session is still valid
        if datetime.now() > created_at + timedelta(seconds=self.session_duration):
            return None
        
        return session_data["user_id"]
