#!/usr/bin/python3
"""Returns a status response"""
from models import storage, CNC
from os import environ
from api.v1.views import app_views
from flask import abort, jsonify, request
STORAGE_TYPE = environ.get('HBNB_TYPE_STORAGE')

@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['DELETE', 'POST'])
def amenity_to_place(place_id=None, amenity_id=None):
    """Handles HTTP methods for adding/removing amenities"""
    place_obj = storage.get('Place', place_id)
    amenity_obj = storage.get('Amenity', amenity_id)

    if not place_obj or not amenity_obj:
        abort(404, 'Not found')

    if request.method == 'DELETE':
        if amenity_obj not in place_obj.amenities:
            abort(404, 'Not found')

        place_obj.amenities.remove(amenity_obj)
        place_obj.save()
        return jsonify({}), 200

    if request.method == 'POST':
        if amenity_obj in place_obj.amenities:
            return jsonify(amenity_obj.to_json()), 200

        place_obj.amenities.append(amenity_obj)
        place_obj.save()
        return jsonify(amenity_obj.to_json()), 201


@app_views.route('/places/<place_id>/amenities', methods=['GET'])
def amenities_per_place(place_id=None):
    """Handles HTTP method for retrieving amenities for a specific place"""
    place_obj = storage.get('Place', place_id)

    if not place_obj:
        abort(404, 'Not found')

    place_amenities = place_obj.amenities

    return jsonify([amenity.to_json() for amenity in place_amenities])
