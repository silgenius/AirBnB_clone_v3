#!/usr/bin/python3

"""
    Module: db_storage

    This module implements the New engine DBStorage, which facilitates the
    stoorage of data into database.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from os import getenv
from models.city import City
from models.state import State
from models.review import Review
from models.place import Place
from models.amenity import Amenity
from models.user import User
from models.base_model import Base
from sqlalchemy.engine.reflection import Inspector


class DBStorage:
    """
    Manages database storage for models using SQLAlchemy.
    """

    __engine = None
    __session = None

    def __init__(self):
        """
        Initializes the database engine and sets up the session.
        """

        password = getenv('HBNB_MYSQL_PWD')
        username = getenv('HBNB_MYSQL_USER')
        database = getenv('HBNB_MYSQL_DB')
        host = getenv('HBNB_MYSQL_HOST')
        env = getenv('HBNB_ENV')

        Db_url = f'mysql+mysqldb://{username}:{password}@{host}/{database}'
        self.__engine = create_engine(Db_url, pool_pre_ping=True)

        if env == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        Queries the database session for all objects of a class or all classes.
        """

        if cls:
            cls_list = []
            cls_list.append(cls)
        else:
            cls_list = [State, City, User, Amenity, Place, Review]

        new_obj = {}
        for cls in cls_list:
            objects = self.__session.query(cls).all()
            if objects:
                for obj in objects:
                    key = f'{obj.__class__.__name__}.{obj.id}'
                    new_obj[key] = obj
        return new_obj

    def new(self, obj):
        """
        Adds the object to the current database session.
        """

        self.__session.add(obj)

    def save(self):
        """
        Commits all changes of the current database session.
        """

        self.__session.commit()

    def delete(self, obj=None):
        """
        Deletes the object from the current database session if not None.
        """

        if obj is not None:
            self.__session.delete(obj)
            self.save()

    def reload(self):
        """
        Reloads data from the database and creates all tables in the database.
        """

        Base.metadata.create_all(self.__engine)
        Session = scoped_session(sessionmaker(
            bind=self.__engine,
            expire_on_commit=False)
            )
        self.__session = Session()

    def close(self):
        """
        call remove() method on the private session attribute (self.__session)
        """
        self.__session.close()
