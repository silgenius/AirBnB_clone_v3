#!/usr/bin/python3

"""
    Module: user
    This module implements the User class, which inherits from BaseModel
    and base respectively.
"""

from sqlalchemy import Column, String
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship, validates
import hashlib


class User(BaseModel, Base):
    """
    This class represents a user with email, password, first name,
    and last name attributes.

    Attributes:
        email (str): The email of the user.
        password (str): The password of the user.
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.
        All attributes defaults to an empty string.
    """

    __tablename__ = 'users'

    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    first_name = Column(String(128), nullable=True)
    last_name = Column(String(128), nullable=True)

    @validates('password')
    def hash_password(self, key, password):
        """
        Compute the MD5 hash of the password
        """
        md5_hash = hashlib.md5(password.encode('utf-8')).hexdigest()
        return md5_hash

    places = relationship(
            "Place",
            backref="user",
            cascade="all, delete-orphan"
            )
    reviews = relationship(
            "Review",
            backref="user",
            cascade="all, delete-orphan"
            )
