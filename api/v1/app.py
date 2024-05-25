#!/usr/bin/python3
"""create Flask instance"""

from os import getenv
from flask import Flask, jsonify
from api.v1.views import app_views
from models import storage

app = Flask(__name__)
app.register_blueprint(app_views)


@app.errorhandler(404)
def pageNotFound(exception):
    """returns a JSON-formatted 404 status code response."""
    return jsonify({"error": "Not found"})


@app.teardown_appcontext
def teardown(exception):
    """method that calls storage.close()"""
    storage.close()


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST", "0.0.0.0")
    port = getenv("HBNB_API_PORT", 5000)
    debug = getenv("DEBUG", 0)

    app.run(host, port, debug=debug, threaded=True)
