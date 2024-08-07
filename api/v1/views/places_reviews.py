#!/usr/bin/python3

"""
This module defines the routes and view functions for managing
places_reviews within a Flask application.
"""

from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models.city import City
from models.reviews import Review
from models.user import User
from models.place import Place
from models import storage


@app_views.route("/places/<string:place_id>/reviews", methods=['GET'])
def get_place_review(place_id):
    """
    Retrieve a list of all reviews for a specific place by place_id.
    """
    places = storage.all(Place).values()
    for place in places:
        if place.id == place_id:
            reviews = storage.all(Review).values()
            review_list = []
            for review in reviews:
                if review.place_id = place_id:
                    review_list.append(review.to_dict())
            return jsonify(review_list)
    abort(404)


@app_views.route("/reviews/<string:review_id>", methods=['GET'])
def get_review(review_id):
    """
    Retrieve a specific review by review_id.
    """
    reviews = storage.all(Review).values()
    for review in reviews:
        if review.id == review_id:
            return jsonify(review.to_dict())
    abort(404)


@app_views.route("/reviews/<string:review_id>", methods=['DELETE'])
def delete_review(review_id):
    """
    Delete a specific review by review_id.
    """
    reviews = storage.all(Review).values()
    for review in reviews:
        if review.id == review_id:
            storage.delete(review)
            return jsonify({}), 200
    abort(404)


@app_views.route("/places/<string:place_id>/reviews", methods=['POST'])
def create_review(place_id):
    """
    Create a new review for a specific place by place_id.
    """
    places = storage.all(Place).values()
    for place in places:
        if place.id == place_id:
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
                    text = data.get("text")
                    if not text:
                        return jsonify({"error": "Missing text"}), 400
                    new_obj = Review()
                    setattr(new_obj, "place_id", place_id)
                    for key, value in data.items():
                        if key not in ["id", "updated_at", "created_at"]:
                            setattr(new_obj, key, value)
                    storage.new(new_obj)
                    storage.save()
                    return jsonify(new_obj.to_dict()), 201
            abort(400)
    abort(404)


@app_views.route("/reviews/<string:review_id>", methods=['PUT'])
def update_review(review_id):
    """
    Update details of a specific review by review_id.
    """
    reviews = storage.all(Review).values()
    for review in reviews:
        if review.id == review_id:
            try:
                data = request.get_json()
            except Exception:
                return jsonify({"error": "Not a JSON"}), 400
            for key, value in data.items():
                if key not in [
                        "id",
                        "updated_at",
                        "created_at",
                        "place_id",
                        "user_id"
                        ]:
                    setattr(city, key, value)
            storage.save()
            return.jsonify(review.to_dict()), 200
    abort(404)
