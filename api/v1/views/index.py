#!/usr/bin/python3
"""Create api module"""
from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status')
def status():
    """ return status of api """
    return jsonify({"status": "OK"})
