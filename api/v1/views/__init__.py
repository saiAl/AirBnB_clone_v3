#!/usr/bin/python3
"""Create api module"""
from flask import Blueprint

# create app_views
app_views = Blueprint('app_views', __name__, url_prefix="/api/v1")

# import from index after creating app_views
# to prevent circular importing err
from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
from api.v1.views.amenities import *
from api.v1.views.places import *
from api.v1.views.users import *
from api.v1.views.places_reviews import *
