#!/usr/bin/python3
"""Retrieves the number of each objects by type:"""

from api.v1.views import app_views
from flask import jsonify, request
from models import storage

@app_views.route('/status', methods=['GET'], strict_slashes=False)
def stat():
    """Returns the status"""
    if request.method == 'GET':
        req = {"status": "OK"}
        return jsonify(req)

@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats():
    """Count of all class objects"""
    if request.method == 'GET':
        return jsonify(amenities=storage.count("Amenity"),
                       reviews=storage.count("Review"),
                       states=storage.count("State"),
                       users=storage.count("User"),
                       cities=storage.count("City"),
                       places=storage.count("Place"))
                   
