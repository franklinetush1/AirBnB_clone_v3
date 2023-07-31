#!/usr/bin/python3
"""Configuration for User objects """

from models import storage
from models.user import User
import hashlib
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request

@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """ Retrieves the list of all User objects """
    users_data = storage.all(User)
    return jsonify([user.to_dict() for user in users_data.values()])


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user_by_id(user_id):
    """
    file: yml/users_get.yml
    """
    user_obj = storage.get("User", user_id)
    if not user_obj:
        abort(404)
    return jsonify(user_obj.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """ Deletes a User object """
    user_obj = storage.get("User", user_id)
    if not user_obj:
        abort(404)
    user_obj.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    """ Creates a User object """
    new_user_data = request.get_json()
    if not new_user_data:
        abort(400, "Not a JSON")
    if "email" not in new_user_data:
        abort(400, "Missing email")
    if "password" not in new_user_data:
        abort(400, "Missing password")

    user_obj = User(**new_user_data)
    storage.new(user_obj)
    storage.save()
    return make_response(jsonify(user_obj.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def put_user(user_id):
    """ Updates a User object """
    user_obj = storage.get("User", user_id)
    if not user_obj:
        abort(404)

    body_request = request.get_json()
    if not body_request:
        abort(400, "Not a JSON")

    for key, value in body_request.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user_obj, key, value)

    storage.save()
    return make_response(jsonify(user_obj.to_dict()), 200)
