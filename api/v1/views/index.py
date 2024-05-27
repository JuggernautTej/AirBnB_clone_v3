#!/usr/bin/python3
"""index file"""

from flask import jsonify
from api.v1.views import app_views
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """returns a JSON: "status":"OK" """
    return jsonify({"status": "OK"}), 200

@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def obj_count():
    """an endpoint that retrieves the number of objects by type"""

    cls = {"users": User, "places": Place, "cities": City,
           "states": State, "amenities": Amenity, "reviews": Review}
    dict_holder = {}
    for key, value in classes.items():
        dict_holder[key] = storage.count(value)
    return jsonify(new_dict)
