#!/usr/bin/python3
""" Handles all default RESTful actions"""

from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def all_state_objs():
    """Retrieves the list of all state objects"""
    all_states = storage.all(State)
    list_state = [state.to_dict() for state in all_states.values()]
    return jsonify(list_state), 200


@app_views.route("/api/v1/states/<state_id>",
                 methods=["GET"], strict_slashes=False)
def state_objs(state_id):
    """This retrieves a single state object"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict()), 200


@app_views.route("/api/v1/states/<state_id>",
                 methods=["DELETE"], strict_slashes=False)
def del_state(state_id):
    """Delects state objext"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    state.delete()
    storage.save()

    return jsonify({}), 200


@app_views.route("/api/v1/states", methods=["POST"], strict_slashes=False)
def creates_state():
    """creates a state object"""
    try:
        state = request.get_json()
    except Exception as e:
        abort(400, description="Not a JSON")
    if 'name' not in state:
        abort(400, description="Missing name")
    new_obj = State(**state)
    storage.new(new_obj)
    storage.save()
    return jsonify(new_obj.to_dict()), 201


@app_views.route("/api/v1/states/<state_id>",
                 methods=["PUT"], strict_slashes=False)
def update_state(state_id):
    """This updates the state object"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    try:
        data = request.get_json()
    except Exception as e:
        abort(400, description="Not a JSON")
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200
