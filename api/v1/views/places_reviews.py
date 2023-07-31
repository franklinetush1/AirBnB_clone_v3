#!/usr/bin/python3
""" View for Review objects that handles default API actions """
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.place import Place
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def review(place_id):
    """ Gets a list of all Reviews"""
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    return jsonify([review.to_dict() for review in place.reviews])


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def with_review_id(review_id):
    """ Retrieves a Review"""
    review = storage.get("Review", review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/places/<place_id>/reviews', methods=['POST'], strict_slashes=False)
def post_a_review(place_id):
    """Creates a Review object"""
    place = storage.get("Place", place_id)
    if not place:
        abort(404)

    new_review_data = request.get_json()
    if not new_review_data or not all(key in new_review_data for key in ["user_id", "text"]):
        abort(400, "Invalid data format. 'user_id' and 'text' are required.")

    user_id = new_review_data['user_id']
    if not storage.get("User", user_id):
        abort(404, "User not found.")

    review = Review(**new_review_data)
    setattr(review, 'place_id', place_id)
    storage.new(review)
    storage.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def put_a_review(review_id):
    """ Updates a Review """
    review = storage.get("Review", review_id)
    if not review:
        abort(404)

    body_request = request.get_json()
    if not body_request:
        abort(400, "Not a JSON")

    for key, value in body_request.items():
        if key not in ['id', 'user_id', 'place_id',
                     'created_at', 'updated_at']:
            setattr(review, key, value)

    storage.save()
    return make_response(jsonify(review.to_dict()), 200)

@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_a_review(review_id):
    """Deletes a Review"""
    review = storage.get("Review", review_id)
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200
