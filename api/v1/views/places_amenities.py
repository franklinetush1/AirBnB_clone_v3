#!/usr/bin/python3
"""Returns a status response"""
from models import storage, CNC
from os import environ
from api.v1.views import app_views
from flask import abort, jsonify, request
STORAGE_TYPE = environ.get('HBNB_TYPE_STORAGE')

@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['DELETE', 'POST'])
def manage_amenity(place_id=None, amenity_id=None):
    """Handles HTTP methods for adding/removing amenities."""
    place = storage.get('Place', place_id)
    amenity = storage.get('Amenity', amenity_id)

    if not place or not amenity:
        abort(404, 'Place or Amenity not found.')

    if request.method == 'DELETE':
        if amenity not in place.amenities:
            abort(404, 'Amenity not associated with the place.')

        place.amenities.remove(amenity)
        place.save()
        return jsonify({}), 200

    if request.method == 'POST':
        if amenity in place.amenities:
            return jsonify(amenity.to_json()), 200

        place.amenities.append(amenity)
        place.save()
        return jsonify(amenity.to_json()), 201


@app_views.route('/places/<place_id>/amenities', methods=['GET'])
def amenities_per_place(place_id=None):
    """Handles HTTP method for retrieving amenities for a specific place"""
    place_obj = storage.get('Place', place_id)

    if not place_obj:
        abort(404, 'Not found')

    place_amenities = place_obj.amenities

    return jsonify([amenity.to_json() for amenity in place_amenities])
