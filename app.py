from flask_cors import CORS
from flask import Flask
from flask_jwt_extended import JWTManager
import os
import pymysql
from flask_login import LoginManager
from db import db
from oa import oauth

from models.user import User
from auth import auth as auth_blueprint
from aws_lambda import lam as lam_blueprint
from resources.github_login import bp as oauth_blueprint

app = Flask(__name__)
CORS(app)

jwt = JWTManager(app)

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
app.secret_key = 'it-is-hard-to-guess'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
Config.init_app(app)
db.init_app(app)
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

app.register_blueprint(auth_blueprint, url_prefix='/auth')
app.register_blueprint(lam_blueprint, url_prefix='/lam')
app.register_blueprint(oauth_blueprint, url_prefix='/oauth')


@app.before_first_request
def create_tables():
    db.create_all()


if __name__ == '__main__':
    db.init_app(app)
    oauth.init_app(app)
    app.run(host="0.0.0.0", debug=True, port=5011)












