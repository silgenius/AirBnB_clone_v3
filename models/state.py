#!/usr/bin/python3

"""
    Module: state

    This module implements the State class, which inherits from BaseModel.
"""

from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String
from .city import City
from os import getenv


class State(BaseModel, Base):
    """
    Represents a state where cities are located.
    """
    __tablename__ = 'states'

    name = Column(String(128), nullable=False)

    storage_type = getenv('HBNB_TYPE_STORAGE')
    if storage_type == 'db':
        cities = relationship(
            "City",
            backref="state",
            cascade="all, delete-orphan"
            )
    else:
        @property
        def cities(self):
            from . import storage

            all_cities = storage.all(City)
            result = []
            for city in all_cities.values():
                if city.state_id == self.id:
                    result.append(city)
            return result
