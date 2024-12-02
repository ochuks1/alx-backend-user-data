#!/usr/bin/env python3
"""
User model for the database.
"""

from sqlalchemy import Column, Integer, String
from models.base import Base


class User(Base):
    """
    User model for storing user information.
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False, unique=True)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)
