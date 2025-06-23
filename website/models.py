# NAME: models
# AUTHOR: Patrick Cronin
# Date: 22/06/2025
# Update: 22/06/2025
# Purpose: Define database model for assets, asset class, maintenance and users

from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(255), nullable=False)

class Assetclass(db.Model):
    class_code = db.Column(db.String(2), primary_key=True)
    class_desc = db.Column(db.String(50), nullable=False)

    assets = db.relationship('Asset', backref='assetclass', lazy=True)

class Asset(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    serial_number = db.Column(db.String(50))

    class_code_id = db.Column(db.String(2), db.ForeignKey('assetclass.class_code'), nullable=False)
    maintenance = db.relationship('Maintenance', backref='asset', lazy=True)

class Maintenance(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    maintenance_type = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=func.now())

    asset_id = db.Column(db.Integer, db.ForeignKey('asset.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)