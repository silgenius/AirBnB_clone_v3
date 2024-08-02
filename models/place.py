#!/usr/bin/python3

"""
    Module: place

    This module implements the Place class, which inherits from BaseModel
    and Base respectively.
"""

from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, Float, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from os import getenv

"""
    This is a Table for creating the relationship
    Many-To-Many between Place and Amenity
    attributes:
    place_id (str):the id of the place never NULL.
    amenity_id (str): the id of the amenity never NULL.
"""
place_amenity = Table(
        "place_amenity",
        Base.metadata,
        Column(
            "place_id",
            String(60),
            ForeignKey("places.id"),
            primary_key=True,
            nullable=False),
        Column(
            "amenity_id",
            String(60),
            ForeignKey("amenities.id"),
            primary_key=True,
            nullable=False)
        )


class Place(BaseModel, Base):
    """
    Represents a place available for booking.

    Attributes:
            city_id (str): The id of the city.
            user.id (str): The id of the user.
            name (str): The name of the place
            description (str): The description of the place.
            number_rooms (int): The number of rooms in the place.
            number_bathrooms (int): The number of bathrooms in the place.
            max_guest (int): The number of maximum guets held in the place.
            price_by_night (float): The price of the place by night
            latitude (float): Of the place.
            longitude (float): Of the place.
            amenity_ids (list) : list of amenities ids.
    """

    __tablename__ = 'places'

    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, default=0, nullable=False)
    number_bathrooms = Column(Integer, default=0, nullable=False)
    max_guest = Column(Integer, default=0, nullable=False)
    price_by_night = Column(Integer, default=0, nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    storage_type = getenv('HBNB_TYPE_STORAGE')

    if storage_type == 'db':
        reviews = relationship(
                "Review",
                cascade="all, delete",
                backref="place"
                )
    else:
        @property
        def reviews(self):
            """This is a getter attribute reviews that returns the list
            of Review instances with place_id equals to the current Place.id"""

            from models import storage

            result = []
            review_insts = storage.all(Review)
            for review in review_insts.values():
                if review.place_id == self.id:
                    result.append(review)

            return result

    if storage_type == 'db':
        amenities = relationship(
                'Amenity',
                secondary="place_amenity",
                backref="place_amenities",
                viewonly=False
                )
    else:
        @property
        def amenities(self):
            """Getter attribute amenities that returns the list of Amenity
            instances"""
            from models import storage

            return [
                    storage.get('Amenity', amenity_id)
                    for amenity_id in self.amenity_ids
                    ]

        @amenities.setter
        def amenities(self, obj):
            """Setter attribute amenities that handles append method for
            adding an Amenity.id"""

            if isinstance(obj, Amenity):
                self.amenity_ids.append(obj.id)
