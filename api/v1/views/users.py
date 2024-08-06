#!/usr/bin/python3

from flask import Flask, request, jsonify, abort
from api.v1.views import app_views
from models.user import User
from models import storage

<<<<<<< HEAD
app = Flask(__name__)
@app_views.route("/users/<user_id>", methods=['GET', 'DELETE', 'PUT'])
def users_with_id(user_id):
    """A route handles RUD http requests on a user instance with id"""
    user_inst = storage.get(User, user_id)
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
        json.pop("email", None)
        user_inst.update(**json_req)
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
=======

@app_views.route("/users", methods=['GET'])
def all_users():
    users = storage.all(User).values()
    user_list = []
    for user in users:
        user_list.append(user.to_dict())
    return jsonify(user_list)


@app_views.route("/users/<string:user_id>", methods=['GET'])
def get_user(user_id):
    users = storage.all(User).values()
    for user in users:
        if user.id == user_id:
            return jsonify(user.to_dict())
    abort(404)


@app_views.route("/users/<string:user_id>", methods=['DELETE'])
def delete_user(user_id):
    users = storage.all(User).values()
    for user in users:
        if user.id == user_id:
            storage.delete(user)
            return jsonify({}), 200
    abort(404)


@app_views.route("/users", methods=['POST'])
def create_user():
    try:
        data = request.data_json()
    except Exception:
        return jsonify({"error": "Not a JSON"}), 400
    
    email = data.get("email")
    if not email:
        return jsonify({"error": "Missing email"}), 400
    password = data.get("password")
    if not password:
        return jsonify({"error": "Missing password"}), 404

    new_obj = User()
    for key, value in data.items():
        if key == "id" or key == "updated_at" or key == "created_at":
            pass
        else:
            setattr(new_obj, key, value)
    storage.new(new_obj)
    storage.save()

    return jsonify(new_obj.to_dict()), 201


@app_views.route("/users/<string:user_id>", methods=['PUT'])
def update_user(user_id):
    users = storage.all(User).values()
    for user in users:
        if user.id == user_id:
            try:
                data = request.get_json()
            except Exception:
                return jsonify({"error": "Not a JSON"}), 404
            for key, value in data.items():
                if key == "id" or key == "updated_at" or key == "created_at" or key =="email":
                    pass
                else:
                    setattr(user, key, value)
            storage.save()
            return jsonify(user.to_dict()), 200
    abort(404)
>>>>>>> b95f632d1d88a0bbee6ba3f4c9e71faad45eac99
