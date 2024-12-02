#!/usr/bin/env python3
"""
UserSession model for managing session IDs.
"""

from sqlalchemy import Column, String
from models.base import Base


class UserSession(Base):
    """
    UserSession model for session-based authentication.
    """
    __tablename__ = 'user_sessions'

    id = Column(String(250), primary_key=True)
    user_id = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=False)
