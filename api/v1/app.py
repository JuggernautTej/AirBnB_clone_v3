#!/usr/bin/python3
"""Some comment"""

from flask import Flask, jsonify, make_response
from models import storage
from api.v1.views import app_views
import os

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def storage_close(errs):
    """This method calls the close method when an
    exception or error is encountered"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """This method handles error 404"""
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    if os.getenv("HBNB_API_HOST") is not None:
        HBNB_API_HOST = os.getenv("HBNB_API_HOST")
    else:
        HBNB_API_HOST = '0.0.0.0'
    if os.getenv("HBNB_API_PORT") is not None:
        HBNB_API_PORT = int(os.getenv("HBNB_API_PORT"))
    else:
        HBNB_API_PORT = 5000
    app.run(host=HBNB_API_HOST, port=HBNB_API_PORT, threaded=True)
