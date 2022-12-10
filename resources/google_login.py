from flask import url_for, g, request, session, jsonify
import os
from oa import oauth
from models.user import User
from flask_jwt_extended import create_access_token
import json
from flask import Blueprint
import requests
from models.user import User
import uuid
from db import db

bp = Blueprint('oauth', __name__)

@bp.route('/google')
def google():
    rsp = requests.get(url_for('oauth2.google_login', _external=True))
    print(rsp.content)
    rsp.headers['Access-Control-Allow-Origin'] = '*'
    return "hhh"


