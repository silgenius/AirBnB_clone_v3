#!/usr/bin/python3

from flask import Flask, request, jsonify, abort
from api.v1.views import app_views
from models.user import User
from models import storage

app = Flask(__name__)
user_inst = storage.get(User, user_id)

@app_views.route("/users/<user_id>", methods=['GET', 'DELETE', 'PUT'])
def users_with_id(user_id):
    """A route handles RUD http requests on a user instance with id"""
    if not user_inst:
        abort(404, 'Not found')

    """check for HTTP request method"""
    if request.method == 'GET':
        return jsonify(user_inst.to_dict())

    if request.method == 'DELETE':
        user_inst.delete()
        del user_inst
        return jsonify({}), 200

    if request.method == 'PUT':
        json_req = request.get_json()
        if not json_req:
            abort(400, 'Not a JSON')
        user_inst.update(json_req)
        return jsonify(user_inst.to_dict()), 200

@app_views.route("/users/<user_id>", methods=['GET','POST'])
def users_no_id(user_id):
    """A route handles RU http requests on a user instance with no id"""

    """check for HTTP request method"""
    if request.method == 'GET':
        user_insts = storage.all('User').values()
        user_insts =[inst.to_dict() for inst in user_insts]
        return jsonify(user_ints)

    if request.method == 'POST':
        json_req = request.get_jason()
        if not json_req:
            abort(404, 'Not a JSON')
        if not json_req.get('email'):
            abort(400, 'Missing email')
        if not json_req.get('password'):
            abort(400, 'Missing password')
        user = User(**json_req)
        user.save()
        return jsonify(user.to_dict()), 201
