#!/usr/bin/python3

from flask import Flask, jsonify, abort
from api.v1.views import app_views
from models.state import State
from models import storage


app = Flask(__name__)
states = storage.all(State).values()

@app_views.route("/states/", methods=['GET'])
def get_state():
    state_list = []
    for state in states:
        state_list.append(state.to_dict())
    return jsonify(state_list)

@app_views.route("/states/<string:state_id>", methods=['GET'])
def state_with_id(state_id):
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
            return {}
    abort (404)
