#!/usr/bin/env python3
"""
Database management module.
"""

from sqlalchemy import create_engine
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from models.user import User


class DB:
    """
    DB class for database operations.
    """

    def __init__(self):
        self._engine = create_engine("sqlite:///a.db", echo=False)
        User.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self):
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        try:
            user = self._session.query(User).filter_by(**kwargs).first()
            if not user:
                raise NoResultFound
            return user
        except InvalidRequestError:
            raise
        except NoResultFound:
            raise

    def update_user(self, user_id: int, **kwargs) -> None:
        user = self.find_user_by(id=user_id)
        for key, value in kwargs.items():
            if not hasattr(user, key):
                raise ValueError(f"{key} is not a valid attribute of User")
            setattr(user, key, value)
        self._session.commit()
