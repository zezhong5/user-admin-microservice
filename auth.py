from flask import Blueprint, render_template, redirect, url_for, request, flash
from models.user import User
from flask_login import login_user, logout_user, login_required
from app import db, login_manager
auth = Blueprint('auth', __name__)
import uuid

@auth.route('/login')
def login():
  return render_template('login.html')

@auth.route('/login', methods=['POST'])
def user_login():
  email = request.form.get('email')
  password = request.form.get('password')
  remember = True if request.form.get('remember') else False
  user = User.query.filter_by(email=email).first()
  if not user or not user.verify_password(password):
      flash('Please check your login details and try again.', 'danger')
      return redirect(url_for('auth.login'))

  login_user(user, remember = remember)
  flash('You are now logged in. Welcome back!', 'success')
  return redirect(url_for('main.profile'))


@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    user = User.query.filter_by(email=email).first()
    if user:
        flash('Email address already registered')
        return redirect(url_for('auth.signup'))
    new_user = User(username = username, email = email,
                    password = password, first_name = first_name,
                    last_name = last_name,id = uuid.uuid4())
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
  logout_user()
  return redirect(url_for('main.index'))










