#!/usr/bin/python3

from flask import Flask, request, jsonify, abort
from api.v1.views import app_views
from models.amenity import Amenity
from models import storage

app = Flask(__name__)
amenity_inst = storage.all(Amenity).values()

@app_views.route("/amenities/<amenity_id>", methods=['GET', 'DELETE', 'PUT'])
def amenities_with_id(amenity_id):
    """RUD http requests on a amenity instance with id"""
    if not amenity:
        abort(404)

    """check for HTTP request method"""
    if request.method == 'GET':
        return jsonify(amenity.to_dict())

    if request.method == 'DELETE':
        amenity_inst.delete()
        del amenity_inst
        return jsonify({}), 200

    if request.method == 'PUT':
        json_req = request.get_json()
        if not json_req:
            abort(400, 'Not a JSON')
        amenity_inst.update()
        return jsonify(amenity.to_dict()), 200

@app_views.route("/amenities/<amenity_id>", methods=['GET', 'POST'])
def amenities_no_id(amenity_id):
    """RU http request on a amenity instance with no id"""

    """check for HTTP request method"""
    if request.method == 'GET':
        all_amenities = [inst.to_dict() for inst in amenity_insts]
        return jsonify(all_amenities)

    if request.method == 'POST':
        json_req = request.get_jason
        if not json_req:
            abort(404, 'Not a JSON')
        if not json_req.get('name'):
            abort(400, 'Missing name')
        amenity_inst = Amenity(**json_req)
        amenity_inst.(save)
        return jsonify(amenity_inst.tod_dict()), 201
