from flask import url_for, g, request, session, jsonify, redirect
import os
from oa import oauth
from models.user import User
from flask_jwt_extended import create_access_token, verify_jwt_in_request, get_jwt
import json
from flask import Blueprint
import requests
from models.user import User
import uuid
from db import db
from flask_cors import CORS

bp = Blueprint('oauth', __name__)
CORS(bp)


@bp.route('/login/github')
def github_login():
    print(url_for("oauth.github_authorize"))
    rsp = oauth.github.authorize_redirect(url_for("oauth.github_authorize",  _external=True))
    print(rsp)
    return rsp

@bp.route('/login/github/authorized')
def github_authorize():
    print("here")
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

    return {"access_token": access_token, "email": primary_email, "user": user.to_dict()}, 200

@bp.route('/login/google/')
def google_login():
    redirect_url = url_for("oauth.google_authorize",  _external=True)
    rsp = oauth.google.authorize_redirect(redirect_url)
    print(rsp.location)
    return rsp

@bp.route('/login/google/authorize/')
def google_authorize():
    print("here")
    token = oauth.google.authorize_access_token()
    userInfo = token['userinfo']
    email = userInfo['email']
    if not email:
        return {"message": "Cannot get email information from Google"}, 401
    user = User.find_by_email(email)
    if not user:
        first_name = userInfo['given_name']
        last_name = userInfo['family_name']
        user = User(username=email, email=email, password=None, first_name=first_name, last_name=last_name, id=uuid.uuid4(), confirmed=True)
        user.save_to_db()
    elif not user.confirmed:
        user.confirmed = True
        db.session.commit()
    
    access_token = create_access_token(identity=user.id, fresh=True)

    return redirect(f"http://127.0.0.1:4000/loggedin?token={access_token}")
    return {"access_token": access_token, "email": email, "user": user.to_dict()}, 200

@bp.route('/authorize')
def get_user_from_token():
    verify_jwt_in_request()
    user_id = get_jwt()['sub']
    user = User.find_by_id(user_id)
    return {"user": user.to_dict()}, 200
