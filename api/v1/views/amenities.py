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


@app_views.route("/amenities", methods=['GET'])
def all_amenities():
    amenities = storage.all(Amenity).values()
    amenity_list = []
    for amenity in amenities:
        amenity_list.append(amenity.to_dict())
    return jsonify(amenity_list)

@app_views.route("/amenities/<string:amenity_id>", methods=['GET'])
def get_amenity(amenity_id):
    amenities = storage.all(Amenity).values()
    for amenity in amenities:
        if amenity.id == amenity_id:
            return jsonify(amenity.to_dict())
    abort(404)

@app_views.route("/amenities/<string:amenity_id>", methods=['DELETE'])
def delete_amenity(amenity_id):
    amenities = storage.all(Amenity).values()
    for amenity in amenities:
        if amenity.id == amenity_id:
            storage.delete(amenity_id)
            storage.save()
    abort(404)


@app_views.route("/amenities", methods=['POST'])
def create_amenity():
    try:
        data = request.get_json()
    except Exception:
        return jsonify({"error": "Not a JSON"}), 400

    name = data.get("name")
    if not name:
        return jsonify({"error": "Missing name"}), 400

    new_obj = Amenity()
    for key, value in data.items():
        if key == "id" or key == "updated_at" or key == "created_at":
            pass
        else:
            setattr(new_obj, key, value)
    storage.new(new_obj)
    storage.save()

    return jsonify(new_obj.to_dict()), 201


@app_views.route("/amenities/<string:amenity_id>", methods=['GET'])
def update_amenity(amenity_id):
    amenities = storage.all(Amenity).values()
    for amenity in amenities:
        if amenity.id == amenity_id:
            try:
                data = request.get_json()
            except Exception:
                return jsonify({"error": "Not a JSON"}), 400
            for key, value in data.items():
                if key == "id" or key == "updated_at" or key == "created_at":
                    pass
                else:
                    setattr(user, key, value)
            storage.save()
            return jsonify(user.to_dict()), 200
    abort(404)
