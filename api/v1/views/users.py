#!/usr/bin/python3

from flask import Flask, request, jsonify, abort
from api.v1.views import app_views
from models.user import User
from models import storage


@app_views.route("/users", methods=['GET'])
def all_users():
    """
    Retrieve a list of all users.
    """
    users = storage.all(User).values()
    user_list = []
    for user in users:
        user_list.append(user.to_dict())
    return jsonify(user_list)


@app_views.route("/users/<string:user_id>", methods=['GET'])
def get_user(user_id):
    """
    Retrieve a specific user by user_id.
    """
    users = storage.all(User).values()
    for user in users:
        if user.id == user_id:
            return jsonify(user.to_dict())
    abort(404)


@app_views.route("/users/<string:user_id>", methods=['DELETE'])
def delete_user(user_id):
    """
    Delete a specific user by user_id.
    """
    users = storage.all(User).values()
    for user in users:
        if user.id == user_id:
            storage.delete(user)
            return jsonify({}), 200
    abort(404)


@app_views.route("/users", methods=['POST'])
def create_user():
    """
    Create a new user.
    """
    try:
        data = request.get_json()
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
        if key not in ["id", "updated_at", "created_at"]:
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
                if key not in ["id", "updated_at", "created_at", "email"]:
                    setattr(user, key, value)
            storage.save()
            return jsonify(user.to_dict()), 200
    abort(404)
