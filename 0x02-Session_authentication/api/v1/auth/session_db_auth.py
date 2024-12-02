#!/usr/bin/env python3
""" SessionDBAuth class for managing user sessions in the database. """

from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """ Session authentication class that stores sessions in the database. """

    def create_session(self, user_id=None):
        """ Creates a new session and stores it in the database. """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        
        # Create a UserSession instance
        user_session = UserSession(user_id=user_id, session_id=session_id)
        user_session.save()  # Save to database
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ Returns the user ID based on session ID stored in the database. """
        if session_id is None:
            return None
        user_session = UserSession.search({"session_id": session_id})
        if not user_session:
            return None
        return user_session[0].user_id

    def destroy_session(self, request=None):
        """ Deletes the user session from the database. """
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        user_session = UserSession.search({"session_id": session_id})
        if not user_session:
            return False
        user_session[0].remove()  # Assuming remove method deletes the session
        return True
