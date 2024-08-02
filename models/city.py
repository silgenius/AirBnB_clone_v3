#!/usr/bin/python3

"""
    Module: city

    This module implements the City class, which inherits from BaseModel.
"""

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from models.place import Place


class City(BaseModel, Base):
    """
    Represents a city within a state.
    """
    __tablename__ = 'cities'

    name = Column(String(128), nullable=False)
    state_id = Column(String(60), ForeignKey('states.id'), nullable=False)

    places = relationship(
            'Place',
            backref='cities',
            cascade="all, delete-orphan"
            )
