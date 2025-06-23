# NAME: config
# AUTHOR: Patrick Cronin
# Date: 15/06/2025
# Update: 15/06/2025
# Purpose: DB configuration

class Config:
    SECRET_KEY = 'BUTTERNUT SQUASH'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False