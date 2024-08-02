#!/usr/bin/python3

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
    return jsonify({"status": "OK"})

@app_views.route("/stats")
def stats():
    stat = {
            "amenities": storage.count(Amenity),
            "cities" : storage.count(City),
            "places": storage.count(Place),
            "reviews": storage.count(Review),
            "states" : storage.count(State),
            "users": storage.count(User)
            }
    return jsonify(stat)
