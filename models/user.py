from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from db import db
import jwt
from time import time
import os
import uuid




class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String(128),primary_key = True, default=uuid.uuid4)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    username = db.Column(db.String(150))
    confirmed = db.Column(db.Boolean, default=False)

    def __init__(self, username, password, email, id, confirmed=False):
        self.username =username
        self.email = email
        self.id = id
        self.confirmed = confirmed

        if password:
            self.password_hash = generate_password_hash(password)

    def full_name(self):
        return '%s %s' % (self.first_name, self.last_name)

    @property
    def password(self):
        raise AttributeError('passward is not readable')
    

    def confirm(self):
        self.confirmed = True
        db.session.commit()

    def verify_password(self,passward):
        return check_password_hash(self.password_hash,passward)

    def get_reset_token(self, expires = 500):
        return jwt.encode(
            {'reset_password':self.username, 'exp': time()+expires},
            'zezhong',
            algorithm='HS256'
        )
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def verify_reset_token(token):
        try:
            username = jwt.decode(token,'zezhong',algorithm='HS256')['reset_password']
        except:
            return
        return User.query.filter_by(username = username).first()
    
    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()
    
    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'confirmed': self.confirmed
        }








