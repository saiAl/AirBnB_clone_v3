#!/usr/bin/python3
"""create app instance of Flask\
        register the blueprint app_views to your Flask instance app"""


from os import getenv
from flask import Flask
# from app_views import api.v1.views
from api.v1.views import app_views
# from storage import models
from models import storage

app = Flask(__name__)
app.register_blueprint(app_views)
host = getenv("HBNB_API_HOST", "0.0.0.0")
port = getenv("HBNB_API_PORT", "5000")


@app.teardown_appcontext
def teardown(exception):
    """method that calls storage.close()"""
    storage.close()


if __name__ == "__main__":
    app.run(host, port, threaded=True, debug=True)
