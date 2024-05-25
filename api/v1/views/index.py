#!/usr/bin/python3
""" Create api module """
from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/status')
def status():
    """ return status of api """
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def stats():
    """ retrieves the number of each objects by type """
    from models.amenity import Amenity
    from models.city import City
    from models.place import Place
    from models.review import Review
    from models.state import State
    from models.user import User

    classes = {
            "amenities": Amenity,
            "cities": City,
            "places": Place,
            "reviews": Review,
            "states": State,
            "users": User
            }

    new = {}

    for key, value in classes.items():
        for v in storage.all().values():
            if value.__name__ == v.__class__.__name__:
                count = storage.count(v.__class__.__name__)
                new.update({key: count})

    return jsonify(new)
