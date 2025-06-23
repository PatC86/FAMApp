from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from os import path
import logging



db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    db.init_app(app)

    from .views import  views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Assetclass, Asset, Maintenance

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'

    try:
        login_manager.init_app(app)
        @login_manager.user_loader
        def load_user(id):
            return User.query.get(int(id))
    except Exception as e:
        logging.error(f"Error loading user {id}: {e}")
        return None

    return app

def create_database():
    if not path.exists('database.db'):
        db.create_all()