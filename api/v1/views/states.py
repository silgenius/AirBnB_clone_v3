#!/usr/bin/python3

from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models.state import State
from models import storage


app = Flask(__name__)

@app_views.route("/states/", methods=['GET'])
def get_state():
    states = storage.all(State).values()

    state_list = []
    for state in states:
        state_list.append(state.to_dict())
    return jsonify(state_list)

@app_views.route("/states/<string:state_id>", methods=['GET'])
def state_with_id(state_id):
    states = storage.all(State).values()

    for state in states:
        if state.id == state_id:
            return jsonify(state.to_dict())
    abort(404)

@app_views.route("/states/<string:state_id>", methods=['DELETE'])
def delete_state(state_id):
    states = storage.all(State).values()

    for state in states:
        if state.id == state_id:
            storage.delete(state)
            return {}, 200
    abort (404)

@app_views.route("/states/", methods=['POST'])
def create_state():
    try:
        data = request.get_json()
    except Exception:
        return jsonify({"error": "Not a JSON"}), 400

    name = data.get("name")
    if not name:
        return jsonify({"error": "Missing name"}), 400

    new_state = State()
    for key, value in data.items():
        if key == "id" or key == "created_at" or key == "updated_at":
            pass
        else:
            setattr(new_state, key, value)
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201

@app_views.route("/states/<string:state_id>", methods=['PUT'])
def update_state(state_id):
    states = storage.all(State).values()

    for state in states:
        if state.id == state_id:
            try:
                data = request.get_json()
            except Exception:
                return jsonify({"error": "Not a JSON"}), 400

            for key, value in data.items():
                if key == "id" or key == "created_at" or key == "updated_at":
                    pass
                else:
                    setattr(state, key, value)
            storage.save()
            return jsonify(state.to_dict()), 200

    abort(404)
