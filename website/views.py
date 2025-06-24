# NAME: views
# AUTHOR: Patrick Cronin
# Date: 22/06/2025
# Update: 24/06/2025
# Purpose: Define views/routes for the application

from .models import Assetclass
from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from . import db

ASSET_CLASS_CODE_LENGTH = 2
MINIMUM_ASSET_CLASS_DESC_LENGTH = 5

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    return render_template("home.html", user=current_user)

@views.route('/assets', methods=['GET', 'POST'])
@login_required
def assets():
    return render_template("assets.html", user=current_user)

@views.route('/assetclassadmin', methods=['GET', 'POST'])
@login_required
def assetclassadmin():
    if request.method == 'POST':
        AssetClassCode = request.form.get('asset_class_code')
        AssetClassDesc = request.form.get('asset_class_desc')

        if len(AssetClassCode) != ASSET_CLASS_CODE_LENGTH:
            flash('Asset class code is invalid', category='error')
        elif len(AssetClassDesc) < MINIMUM_ASSET_CLASS_DESC_LENGTH:
            flash('Asset class description is too short', category='error')
        else:
            new_asset_class_code = Assetclass(class_code=AssetClassCode, class_desc=AssetClassDesc)
            db.session.add(new_asset_class_code)
            db.session.commit()
            flash('Asset class code has successfully been created', category='success')


    return render_template("assetclassadmin.html", user=current_user)

@views.route('/maintenance', methods=['GET', 'POST'])
@login_required
def maintenance():
    return render_template("maintenance.html", user=current_user)

