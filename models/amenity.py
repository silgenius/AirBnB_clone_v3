#!/usr/bin/python3

"""
    Module: amenity

    This module implements the Amenity class, which inherits from BaseModel
    and Base respectively.
"""

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from .place import place_amenity


class Amenity(BaseModel, Base):
    """
    This class represents an amenity available in a place.

    Attributes:
            name (str): The name of the amenity.
    """
    __tablename__ = "amenities"

    name = Column(String(128), nullable=False)
