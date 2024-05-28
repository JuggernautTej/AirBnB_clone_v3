#!/usr/bin/python3
""" Handles all default RESTful actions"""

from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City


@app_views.route("/states/<state_id>/cities",
                 methods=["GET"], strict_slashes=False)
def all_cities_objs(state_id):
    """Retrieves the list of all cities of a specific state"""
    state = storage.get(State, state_id)

    if not state:
        abort(404)
    all_cities = [city.to_dict() for city in state.cities]
    return jsonify(all_cities)


@app_views.route("/cities/<city_id>",
                 methods=["GET"], strict_slashes=False)
def city_objs(city_id):
    """This retrieves a city object"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>",
                 methods=["DELETE"], strict_slashes=False)
def del_state(city_id):
    """Deletes city object"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    city.delete()
    storage.save()

    return jsonify({}), 200


@app_views.route("/states/<state_id>/cities",
                 methods=["POST"], strict_slashes=False)
def creates_city(state_id):
    """creates a city object"""
    state = storage.get(State, state_id)

    if not state:
        abort(404)

    try:
        city = request.get_json()
    except Exception:
        abort(400, description="Not a JSON")

    if 'name' not in city:
        abort(400, description="Missing name")

    new_obj = City(**city)
    new_obj.state_id = state_id
    storage.new(new_obj)
    storage.save()
    return jsonify(new_obj.to_dict()), 201


@app_views.route("/cities/<city_id>",
                 methods=["PUT"], strict_slashes=False)
def update_state(city_id):
    """This updates the city object"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    try:
        data = request.get_json()
    except Exception as e:
        abort(400, description="Not a JSON")
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    city.save()
    return jsonify(city.to_dict()), 200
