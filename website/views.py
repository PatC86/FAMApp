# NAME: views
# AUTHOR: Patrick Cronin
# Date: 22/06/2025
# Update: 22/06/2025
# Purpose: Define views/routes for the application

from flask import Blueprint, render_template

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html")

