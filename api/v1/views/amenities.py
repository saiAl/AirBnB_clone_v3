#!/usr/bin/python3
""" view for State objects that handles all RESTFul API actions """

from models.amenity import Amenity
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def all_amenity():
    """ Retrieves the list of all Amenity objects"""
    all_amenities = []
    for amenity in storage.all(Amenity).values():
        all_amenities.append(amenity.to_dict())
    return jsonify(all_amenities)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def amenity(amenity_id):
    """ Retrieves an amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """ Deletes an amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if state is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def new_Amenity():
    """ Creates an amenity  """
    amenity = request.get_json(silent=True)
    if amenity is None:
        abort(400, "Not a JSON")
    if "name" not in amenity:
        abort(400, "Missing name")
    amenity = Amenity(**amenity)
    amenity.save()
    return make_response(jsonify(amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """ Updates an amenity  object """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    update_amenity = request.get_json(silent=True)
    if update_amenity is None:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in update_amenity.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(amenity, key, value)
    amenity.save()
    return make_response(jsonify(amenity.to_dict()), 200)
