import os

from flask import Flask, request, redirect, Blueprint
from flask_sqlalchemy import SQLAlchemy
import os
import pymysql
from flask_login import LoginManager

class Config:
    DEBUG = True
    ASSETS_DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Fzzapp2016@localhost/f22_databases'

    @staticmethod
    def init_app(app):
        pass

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = 'basic'
login_manager.login_view = 'auth.login'

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.secret_key = 'zezhong'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    Config.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    from models.user import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)
    from auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    from main import main as main_blueprint
    app.register_blueprint(main_blueprint,url_prefix='/main')
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)












