# -*- coding: utf-8 -*-
from flask import Blueprint
from flask_cors import CORS

# Flask Blueprint 정의
api = Blueprint('api', __name__)
CORS(api)  # enable CORS on the API_v1.0 blueprint

from . import errors, authentication, news, users, search, stars
