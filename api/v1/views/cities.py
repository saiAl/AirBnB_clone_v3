#!/usr/bin/python3
""" view for City objects that handles all RESTFul API actions """

from models.state import State
from models.city import City
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def all_cities(state_id):
    """ Retrieves the list of all City objects of a State"""
    state = storage.get(State, state_id)
    if state is None:
        return jsonify({"error": "Not found"}), 404

    all_cities = []
    for city in storage.all(City).values():
        if city.state_id == state_id:
            all_cities.append(city.to_dict())
    return jsonify(all_cities)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def city(city_id):
    """ Retrieves a city object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """ Deletes a city object"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def new_city(state_id):
    """ Creates a city  """
    state = storage.get(State, state_id)
    if state is None:
        return jsonify({"error": "Not found"}), 404

    city = request.get_json(silent=True)
    if city is None:
        return jsonify({"error": "Not a JSON"}), 400

    if "name" not in city:
        abort(400, "Missing name")

    city = City(**city)
    city.state_id = state_id
    city.save()

    return make_response(jsonify(city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """ Updates a city object """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    updated_value = request.get_json(silent=True)

    if updated_value is None:
        return jsonify({"error": "Not a JSON"}), 400

    for key, value in updated_value.items():
        if key not in ["id", "state_id", "created_at", "updated_at"]:
            setattr(city, key, value)
    city.save()
    return make_response(jsonify(city.to_dict()), 200)
