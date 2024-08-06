#!/usr/bin/python3
"""
This module defines the routes and view functions for managing
amenities within a Flask application.
Routes:
    -GET /api/v1/places Retrieves the list of all place objects
    -GET /api/v1/places/<amenity_id> Retrieves a place object
    -DELETE /api/v1/places/<amenity_id> Deletes a place object
    -POST /api/v1/places Creates a place
    -PUT /api/v1/palces/<amenity_id> Updates a place object
"""

from flask import Flask, request, jsonify, abort
from api.v1.views import app_views
from models.amenity import Amenity
from models import storage

app = Flask(__name__)
@app_views.route("/places/<place_id>", methods=['GET', 'DELETE', 'PUT'])
def places_with_id(place_id):
    """RUD http requests on a place instance with id"""
    place_inst = storage.all(place)
    place = place_inst.get(place_id)

    if not place:
        abort(404)

    """check for HTTP request method"""
    if request.method == 'GET':
        return jsonify(place.to_dict())
    if request.method == 'DELETE':
        place_inst.delete()
        storage.save()
        return jsonify ({}), 200

@app_views.route("/places/<place_id>", methods=['GET', 'POST'])
def places_no_id(place_id):
    """RU http request on a place instance with no id"""

    """check for HTTP request method"""
    if request.method == 'GET':
        places_all = [inst.to_dict() for inst in storage.all(Place).values()]
        return jsonify(places_all)

    if request.method == 'POST':
        json_req = request.get_jason
        if not json_req:
            abort(404, 'Not a JSON')
        if not json_req.get('name'):
            abort(400, 'Missing name')
        place_inst = Place(**json_req)
        place_inst.save()
        return jsonify(place_inst.to_dict()), 201
