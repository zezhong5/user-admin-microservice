import os
from flask_cors import CORS
from flask import Flask, request, redirect, Blueprint
from flask_sqlalchemy import SQLAlchemy
import os
import pymysql
from flask_login import LoginManager
from db import db

from models.user import User
from auth import auth as auth_blueprint

app = Flask(__name__)
CORS(app)

class Config:
    DEBUG = True
    ASSETS_DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://okcloud:okcloudokcloud@okcloud-requests-database.cw2ylftvdgpn.us-east-1.rds.amazonaws.com/ride_share_user_login_database'

    @staticmethod
    def init_app(app):
        pass



login_manager = LoginManager()
login_manager.session_protection = 'basic'
login_manager.login_view = 'auth.login'


app.config.from_object(Config)
app.secret_key = 'zezhong'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
Config.init_app(app)
db.init_app(app)
login_manager.init_app(app)



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

app.register_blueprint(auth_blueprint, url_prefix='/auth')


@app.before_first_request
def create_tables():
    db.create_all()


if __name__ == '__main__':
    db.init_app(app)
    app.run(debug=True, port=5011)












