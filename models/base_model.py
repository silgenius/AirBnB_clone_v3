#!/usr/bin/python3

"""
    Module: BaseModel

    This module contains the BaseModel class, which serves as a
    foundation for other classes by defining common attributes
    and methods.
"""

import uuid
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime

Base = declarative_base()


class BaseModel:
    """
    BaseModel class defines common attributes/methods for other classes.
    """

    id = Column(String(60), primary_key=True, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __init__(self, *args, **kwargs):
        """
        Initializes a new instance of BaseModel.
        """

        # Reload obj if already exist
        if kwargs and kwargs is not None:
            for key, value in kwargs.items():
                if key == "__class__":
                    pass
                elif key == "updated_at" or key == "created_at":
                    setattr(self, key, datetime.fromisoformat(value))
                else:
                    setattr(self, key, value)

                # Create object if not yet exist
                if self.id is None:
                    self.id = str(uuid.uuid4())
                    self.created_at = datetime.now()
                    self.updated_at = datetime.now()
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()

    def __str__(self):
        """
        Returns a string representation of the BaseModel instance.
        """

        dict_rep = self.__dict__.copy()

        if '_sa_instance_state' in dict_rep:
            dict_rep.pop('_sa_instance_state')

        return ("[{}] ({}) {}"
                .format(
                    self.__class__.__name__,
                    self.id,
                    dict_rep
                    )
                )

    def save(self):
        """
        Updates the updated_at attribute with the current datetime.
        """
        from . import storage

        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """
        Returns a dictionary containing all keys/values of the instance.
        """
        new_dict = self.__dict__.copy()
        new_dict.update({"__class__": self.__class__.__name__})
        new_dict['created_at'] = self.created_at.isoformat()
        new_dict['updated_at'] = self.updated_at.isoformat()

        if '_sa_instance_state' in new_dict.keys():
            new_dict.pop('_sa_instance_state')

        return new_dict

    def delete(self):
        """
        Delete the current instance from the storage
        """

        storage.pop(self)
