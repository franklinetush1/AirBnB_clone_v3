#!/usr/bin/python3
"""Configuration for  Place objects"""
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.city import City
from models.place import Place
import requests
import json
from os import getenv


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def places(city_id):
    """ Retrieves the list of all Place objects """
    city = storage.get("City", city_id)
    if not city:
        abort(404)
    return jsonify([place.to_dict() for place in city.places])


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def place_id(place_id):
    """ Retrieves a Place object """
    place_val = storage.get("Place", place_id)
    if not place_val:
        abort(404)
    return jsonify(place_val.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """ Deletes a Place object """
    place_val = storage.get("Place", place_id)
    if place_val == NULL:
        abort(404)
    place_val.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def post_place(city_id):
    """ Creates a Place object """
    city_val = storage.get("City", city_id)
    if not city_val:
        abort(404)
    new_place = request.get_json()
    if not new_place:
        abort(400, "Not a JSON")
    if "user_id" not in new_place:
        abort(400, "Missing user_id")
    user_id = new_place['user_id']
    if not storage.get("User", user_id):
        abort(404)
    if "name" not in new_place:
        abort(400, "Missing name")
    plc = Place(**new_place)
    setattr(plc, 'city_id', city_id)
    storage.new(place)
    storage.save()
    return make_response(jsonify(plc.to_dict()), 201)


@app_views.route('/states/<state_id>/cities', methods=['POST'], strict_slashes=False)
def create_city(state_id):
    """Creates a City object."""
    target_state = storage.get("State", state_id)
    if not target_state:
        abort(404)

    city_data = request.get_json()
    if not city_data or "name" not in city_data:
        abort(400, "Invalid data. 'name' field is missing or not provided in JSON.")

    city_data['state_id'] = state_id
    new_city = City(**city_data)
    storage.new(new_city)
    storage.save()

    return jsonify(new_city.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Updates a Place object."""
    place = storage.get("Place", place_id)
    if not place:
        abort(404)

    request_data = request.get_json()
    if not request_data:
        abort(400, "Invalid data. Not a JSON.")

    disallowed_fields = ['id', 'user_id', 'city_at', 'created_at', 'updated_at']
    for key, value in request_data.items():
        if key not in disallowed_fields:
            setattr(place, key, value)

    storage.save()
    return jsonify(place.to_dict()), 200
