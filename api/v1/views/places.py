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


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def places_search():
    """Retrieves all Place objects"""
    body_r = request.get_json()
    if not body_r or not any(['states', 'cities', 'amenities'] in body_r):
        places = storage.all(Place).values()
    else:
        places = set()

        if body_r.get('states'):
            states = [storage.get("State", id) for id in body_r.get('states')]
            for state in states:
                places.update(state.cities)

        if body_r.get('cities'):
            cities = [storage.get("City", id) for id in body_r.get('cities')]
            places.update(cities)

        if not places:
            places = set(storage.all(Place).values())

        if body_r.get('amenities'):
            amenity_ids = body_r.get('amenities')
            amenities = [storage.get("Amenity", id) for id in amenity_ids]
            places_copy = places.copy()
            for place in places_copy:
                place_amenities = set([amenity.id for amenity in place.amenities])
                if not set(amenity_ids).issubset(place_amenities):
                    places.remove(place)

    return jsonify([place.to_dict() for place in places])


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def put_place(place_id):
    """ Updates a Place object """
    place = storage.get("Place", place_id)
    if not place:
        abort(404)

    body_request = request.get_json()
    if not body_request:
        abort(400, "Not a JSON")

    for key, value in body_request.items():
        if key not in ['id', 'user_id', 'city_at',
                     'created_at', 'updated_at']:
            setattr(place, key, value)

    storage.save()
    return make_response(jsonify(place.to_dict()), 200)

