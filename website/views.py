# NAME: views
# AUTHOR: Patrick Cronin
# Date: 22/06/2025
# Update: 22/06/2025
# Purpose: Define views/routes for the application

from flask import Blueprint, render_template
from flask_login import login_required, current_user

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    return render_template("home.html", user=current_user)

@views.route('/assets')
@login_required
def assets():
    return render_template("assets.html", user=current_user)

@views.route('/assetclassadmin')
@login_required
def assetclassadmin():
    return render_template("assetclassadmin.html", user=current_user)

