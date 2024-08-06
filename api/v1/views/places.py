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
from models.place import Place
from models.city import City
from models.user import User
from models import storage


@app_views.route("/cities/<string:city_id>/places", methods=['GET'])
def get_places_with_city(city_id):
    cities = storage.all(City).values()
    for city in cities:
        if city.id == city_id:
            places = storage.all(Place).values()
            place_list = []
            for place in places:
                if place.city_id == city_id:
                    place_list.append(place.to_dict())
            return jsonify(place_list)
    abort(404)


@app_views.route("/places/<place_id>", methods=['GET'])
def get_place_with_id(place_id):
    places = storage.all(Place).values()
    for place in places:
        if place.id == place_id:
            return jsonify(place.to_dict())
    abort(404)


@app_views("/places/<place_id>", methods=['DELETE'])
def delete_place(place_id):
    places = storage.all(Place).values()
    for place in places:
        if place.id in place_id:
            storage.delete(place)
            storage.save()
            return jsonify({}), 200
    abort(404)


@app_views("/cities/<city_id>/places", methods=['POST'])
def create_place(city_id):
    cities = storage.all(City).values()
    for city in cities:
        if city.id == city_id:
           try:
               data = request.get_json()
           except Exception:
               return jsonify({"error": "Not a JSON"}), 400
           user_id = data.get("user_id")
           if not user_id:
               return jsonify({"error": "Missing user_id"}), 400
           users = storage.all(User).values()
           for user in users:
               if user.id == user_id:
                   name = data.get("name")
                   if not name:
                       return  jsonify({"error": "Missing name"})
                   new_obj = Place()
                   setattr(new_obj, "city_id", city_id)
                   for key, value in data.items():
                       if key == "id" or key == "updated_at" or key == "created_at":
                           pass
                       else:
                           setattr(new_obj, key, value)
                    storage.new(new_obj)
                    storage.save()
                    return jsonify(new_obj.to_dict()), 201
            abort(404)
    abort(404)


@app_views("/places/<place_id>", methods=['PUT'])
def update_place(place_id):
    places = storage.all(Place).values()
    for place in places:
        if place.id == place_id:
            try:
                data = request.get_json()
            except Exception:
                return jsonify({"error": "Not a JSON"}), 400
            for key, value in data.items():
                if key == "id" or key == "updated_at" or key == "created_at" key == " city_id" or key == "user_id":
                    pass
                else:
                    setattr(city, key, value)
            storage.save()
            return.jsonify(place.to_dict()), 200
    abort(404)
