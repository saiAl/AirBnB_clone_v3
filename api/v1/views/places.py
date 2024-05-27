#!/usr/bin/python3
""" view for Place objects that handles all RESTFul API actions """

from models.city import City
from models.place import Place
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def all_places(city_id):
    """ Retrieves the list of all Place objects of a City"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    all_places = []
    for place in storage.all(Place).values():
        if place.city_id == city_id:
            all_places.append(place.to_dict())
    return jsonify(all_places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def place(place_id):
    """ Retrieves a place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """ Deletes a place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def new_place(city_id):
    """ Creates a place  """
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    place = request.get_json(silent=True)
    if place is None:
        return jsonify({"error": "Not a JSON"}), 400
    if "user_id" not in place:
        abort(400, "Missing user_id")
    user = storage.get(User, place.user_id)
    if user is None:
        abort(404)
    if "name" not in place:
        abort(400, "Missing name")
    place = Place(**place)
    place.save()
    return make_response(jsonify(place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """ Updates a place object """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    update_place = request.get_json(silent=True)
    if update_place is None:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in update_place.items():
        if key not in ["id", "user_id", "city_id", "created_at", "updated_at"]:
            setattr(place, key, value)
    place.save()
    return make_response(jsonify(place.to_dict()), 200)
