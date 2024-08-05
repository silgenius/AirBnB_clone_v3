#!/usr/bin/python3
"""
This module defines the routes and view functions for managing
amenities within a Flask application.
Routes:
    -GET /api/v1/amenities Retrieves the list of all Amenity objects
    -GET /api/v1/amenities/<amenity_id> Retrieves a Amenity object
    -DELETE /api/v1/amenities/<amenity_id> Deletes a Amenity object
    -POST /api/v1/amenities Creates a Amenity
    -PUT /api/v1/amenities/<amenity_id> Updates a Amenity object
"""

from flask import Flask, request, jsonify, abort
from api.v1.views import app_views
from models.amenity import Amenity
from models import storage

app = Flask(__name__) 
@app_views.route("/amenities/<amenity_id>", methods=['GET', 'DELETE', 'PUT'])
def amenities_with_id(amenity_id):
    """RUD http requests on a amenity instance with id"""
    amenity_inst = storage.all(Amenity)
    amenity = amenity_inst.get(amenity_id)

    if not amenity:
        abort(404)

    """check for HTTP request method"""
    if request.method == 'GET':
        return jsonify(amenity.to_dict())

    if request.method == 'DELETE':
        amenity_inst.delete()
        storage.save
        return jsonify({}), 200

    if request.method == 'PUT':
        json_req = request.get_json()
        if not json_req:
            abort(400, 'Not a JSON')
        for k, v in json_req.items():
            if k not in ['id'. 'created_at', 'updated_at']
                setattr(amenity, k, v)
        storage.save()
        return jsonify(amenity.to_dict()), 200

@app_views.route("/amenities/<amenity_id>", methods=['GET', 'POST'])
def amenities_no_id(amenity_id):
    """RU http request on a amenity instance with no id"""

    """check for HTTP request method"""
    if request.method == 'GET':
        amenities_all = [inst.to_dict() for inst in storage.all(Amenity).values()]
        return jsonify(amenities_all)

    if request.method == 'POST':
        json_req = request.get_jason
        if not json_req:
            abort(404, 'Not a JSON')
        if not json_req.get('name'):
            abort(400, 'Missing name')
        amenity_inst = Amenity(**json_req)
        amenity_inst.save()
        return jsonify(amenity_inst.to_dict()), 201
