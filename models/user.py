from flask import current_app
from flask_login import AnonymousUserMixin, UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from app import db
import jwt
from time import time
import os

from app import app


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key = True)
    first_name = db.Column(db.String(64), index=True)
    last_name = db.Column(db.String(64), index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    username = db.Column(db.String(150))
    confirmed = db.Column(db.Boolean, default=False)

    def full_name(self):
        return '%s %s' % (self.first_name, self.last_name)

    @property
    def password(self):
        raise AttributeError('passward is not readable')

    @password.setter
    def password(self,password):
        self.password_hash =generate_password_hash(password)

    def verify_password(self,passward):
        return check_password_hash(self.password_hash,passward)

    def get_reset_token(self, expires = 500):
        return jwt.encode(
            {'reset_password':self.username, 'exp': time()+expires},
            app.secret_key,
            algorithm='HS256'
        )

    @staticmethod
    def verify_reset_token(token):
        try:
            username = jwt.decode(token,app.secret_key,algorithm='HS256')['reset_password']
        except:
            return
        return User.query.filter_by(username = username).first()








