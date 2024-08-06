#!/usr/bin/python3

from flask import Flask, request, jsonify, abort
from api.v1.views import app_views
from models.user import User
from models import storage


@app_views("/users", methods=['GET'])
def all_users():
    users = storage.all(User).values()
    user_list = []
    for user in users:
        user_list.append(user.to_dict())
    return jsonify(user_list)


@app_views("/users/<user_id>", methods=['GET'])
def get_user(user_id):
    users = storage.all(User).values()
    for user in users:
        if user.id == user_id:
            return jsonify(user.to_dict())
    abort(404)


@app_views("/users/<user_id>" methods=['DELETTE'])
def delete_user(user_id):
    users = storage.all(User).values()
    for user in users:
        if user.id == user_id:
            storage.delete(user)
            return jsonify({}), 200
    abort(404)


@app_views("/users", methods=['POST'])
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
    storage.save(new_obj)

    return jsonify(new_obj.to_dict()), 201


@app_views("/users/<user_id>", methods=['PUT'])
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
