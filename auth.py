from flask import Blueprint, render_template, redirect, url_for, request, flash
from models.user import User
from flask_login import login_user, logout_user, login_required, current_user
from db import db
auth = Blueprint('auth', __name__)
import uuid
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from sns import SnsWrapper

@auth.route('/login')
def login():
  return render_template('login.html')

@auth.route('/')
def authenticate():
    """
    Authenticates a user.
    """
    if current_user.is_authenticated:
        print('still auth')
        return current_user.to_dict()
    return {'errors': ['Unauthorized']}


@auth.route('/login', methods=['POST'])
def user_login():
    data = request.form
    email = data['email']
    password = data['password']
    user = User.query.filter_by(email=email).first()
    if not user or not user.verify_password(password):
        flash('Please check your login details and try again.', 'danger')
        return {'msg': 'Please check your login details and try again.'}, 401
    if not user.confirmed:
        print(user.confirmed)
        return {'msg': 'please verify your email...'}, 401

    token = create_access_token(identity=user.id)
    rsp = {}
    rsp["user"] = user.to_dict()
    rsp["access_token"] = token
    return rsp, 200


@auth.route('/signup')
def signup():
    return render_template('signup.html')

def generate_confirmation_link(username, registered_id):
    return url_for("auth.verify", _external=True, username=username, hash=registered_id)

@auth.route('/verify', methods=['GET', 'POST'])
def verify():
    username = request.args.get('username', default="", type=str)
    registered_id = request.args.get('hash', default="", type=str)
    # check if user and id is in db
    user = User.query.filter_by(username=username, id=registered_id).first()
    if not user:
        return {"message": "User hasn't been registered."}, 401
    # if so set confirmed to true
    user.confirm()
    return {"message": "User email confirmed. Account is activated."}, 200

@auth.route('/signup', methods=['POST'])
def signup_post():
    data = request.form
    username = data['username']
    email = data['email']
    password = data['password']
    user = User.query.filter_by(email=email).first()
    if user:
        return {"message": "Email has already been used."}, 401

    registered_id = uuid.uuid4()
    new_user = User(username = username, email = email,
                    password = password, id = registered_id)
    db.session.add(new_user)
    db.session.commit()

    # publish to SNS topic for email confirmation
    confirmation_link = generate_confirmation_link(username, registered_id)
    SnsWrapper.PublishRegConfirmTopic(confirmation_link, email)

    # TODO: add step for checking CONFIRMED field when logging in 

    return {"message": "User successfully signed up, please check email for confirmation link"}, 200

@auth.route('/logout', methods=['GET'])
@jwt_required()
def logout():
    user = get_jwt()['sub']
    return {'message': 'User {} logged out'.format(user)}, 200


@auth.route('/userinfo')
@jwt_required()
def get_userinfo():
    user_id = get_jwt()['sub']
    user = User.find_by_id(user_id)
    if not user:
        return {'msg': 'Cannot get user info from database'}, 401

    return user.to_dict(), 200








