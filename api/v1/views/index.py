#!/usr/bin/python3

"""
This module defines additional routes for the Flask application,
focusing on system status and statistics.
"""

from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


@app_views.route("/status")
def status():
    """
        Retrieves the status of the API.
    """
    return jsonify({"status": "OK"})


@app_views.route("/stats")
def stats():
    """
        Retrieves statistics about the number of objects in each model.
    """
    stat = {
            "amenities": storage.count(Amenity),
            "cities": storage.count(City),
            "places": storage.count(Place),
            "reviews": storage.count(Review),
            "states": storage.count(State),
            "users": storage.count(User)
            }
    return jsonify(stat)
