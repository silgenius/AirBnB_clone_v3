#!/usr/bin/python3

from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models.city import City
from models.state import State
from models import storage


app = Flask(__name__)

@app_views.route("states/<string:state_id>/cities", methods=['GET'])
def get_cities_state(state_id):
    states = storage.all(State).values()
    for state in states:
        if state.id == state_id:
            cities = storage.all(City).values()
            city_list = []
            for city in cities:
                if city.state_id == state_id:
                    city_list.append(city.to_dict())
            return jsonify(city_list)

    abort(404)


@app_views.route("/cities/<string:city_id>", methods=['GET'])
def get_city(city_id):
    cities = storage.all(City).values()
    for city in cities:
        if city.id == city_id:
            return jsonify(city.to_dict())
    abort(404)


@app_views.route("/cities/<string:city_id>", methods=['DELETE'])
def delete_city(city_id):
    cities = storage.all(City).values()

    for city in cities:
         if city.id == city_id:
             storage.delete(city)
             return {}, 200
    abort (404)


@app_views.route("/states/<string:state_id>/cities", methods=['POST'])
def create_city(state_id):
    states = storage.all(State).values()
    state_obj = None
    for state in states:
        if state.id == state_id:
            state_obj = state
            break
    if not state_obj:
        abort (404)

    try:
        data = request.get_json()
    except Exception:
        return jsonify({"error": "Not a JSON"}), 400

    name = data.get("name")
    if not name:
        return jsonify({"error": "Missing name"}), 400
    
    new_obj = City()
    setattr(new_obj, "state_id", state_id)
    for key, value in data.items():
        if key == "id" or key == "updated_at" or key == "created_at":
            pass
        else:
            setattr(new_obj, key, value)

    storage.new(new_obj)
    storage.save()

    return jsonify(new_obj.to_dict()), 201


@app_views.route("cities/<string:city_id>", methods=['PUT'])
def update_city(city_id):
    cities = storage.all(City).values()

    for city in cities:
        if city.id == city_id:
            try:
                data = request.get_json()
            except Exception:
                return ({"error": "Not a JSON"}), 400

            for key, value in data.items():
                if key == "id" or key == "updated_at" or key == "created_at":
                    pass
                else:
                    setattr(city, key, value)
            storage.save()

            return jsonify(city.to_dict()), 200

    abort(404)
