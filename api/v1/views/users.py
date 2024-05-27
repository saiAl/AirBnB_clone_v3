#!/usr/bin/python3
""" view for User objects that handles all RESTFul API actions """

from models.user import User
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def all_users():
    """ Retrieves the list of all User objects"""
    all_users = []
    for user in storage.all("User").values():
        all_users.append(user.to_dict())
    return jsonify(all_users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def user(user_id):
    """ Retrieves a User object"""
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """ Deletes a user object"""
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def new_user():
    """ Creates a user  """
    user = request.get_json()
    if user is None:
        abort(400, "Not a JSON")
    if "email" not in user:
        abort(400, "Missing email")
    if "password" not in user:
        abort(400, "Missing password")
    user = User(**user)
    user.save()
    return make_response(jsonify(user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """ Updates a User object """
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    update_user = request.get_json()
    if update_user is None:
        abort(400, "Not a JSON")
    for key, value in update_user.items():
        if key not in ["id", "email", "created_at", "updated_at"]:
            setattr(user, key, value)
    user.save()
    return make_response(jsonify(user.to_dict()), 200)
