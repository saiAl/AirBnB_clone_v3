#!/usr/bin/python3
""" view for State objects that handles all RESTFul API actions """

from models.state import State
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route('/stats', methods=['GET'])
def all_stats():
    """ Retrieves the list of all State objects"""
    all_states = []
    for state in storage.all("State").values():
        all_states.append(state.to_dict())
    return jsonify(all_states)


@app_views.route('/stats/<state_id>', methods=['GET'])
def state(state_id):
    """ Retrieves a State object"""
    state = storage.get("State", state_id)
    if state:
        return jsonify(state.to_dict())
    else:
        abort(404)


@app_views.route('/stats/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """ Deletes a State object"""
    state = storage.get("State", state_id)
    if state:
        storage.delete(state)
        storage.save()
        return make_response(jsonify({}), 200)
    else:
        abort(404)


@app_views.route('/states', methods=['POST'])
def new_state():
    """ Creates a State  """
    state = request.get_json()
    if state is None:
        abort(400, "Not a JSON")
    if "name" not in state:
        abort(400, "Missing name")
    state = State(**state)
    state.save()
    return make_response(jsonify(state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    """ Updates a State object """
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    update_state = request.get_json()
    if update_state is None:
        abort(400, "Not a JSON")
    for key, value in update_state.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(state, key, value)
    state.save()
    return make_response(jsonify(state.to_dict()), 200)
