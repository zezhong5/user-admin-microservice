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


@bp.route('/login/github')
def github_login():
    print(url_for("oauth.github_authorize"))
    return oauth.github.authorize_redirect(url_for("oauth.github_authorize",  _external=True))

@bp.route('/login/github/authorized')
def github_authorize():
    token = oauth.github.authorize_access_token()
    if token is None:
        error_response = {
            "error": "Error getting token",
            "error_description": "Error getting token",
        }
        return error_response, 401

    resp = oauth.github.get("user/emails")
    emails = json.loads(resp.text)
    primary_email = None
    for e in emails:
        if e["primary"]:
            primary_email = e["email"]
    if primary_email is None:
        return {"message": "Cannot get email information from github"}, 401
    
    user = User.find_by_email(primary_email)
    if not user:
        user = User(username=primary_email, email=primary_email, password=None, first_name=None, last_name=None, id=uuid.uuid4(), confirmed=True)
        user.save_to_db()
    elif not user.confirmed:
        user.confirmed = True
        db.session.commit()
    

    access_token = create_access_token(identity=user.id, fresh=True)
    return {"access_token": access_token, "email": primary_email}, 200

