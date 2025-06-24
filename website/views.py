# NAME: views
# AUTHOR: Patrick Cronin
# Date: 22/06/2025
# Update: 24/06/2025
# Purpose: Define views/routes for the application

from .models import Assetclass, Asset, Maintenance
from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from . import db

ASSET_CLASS_CODE_LENGTH = 2
MINIMUM_DESC_LENGTH = 5
ASSET_STATUSES = ['IN SERVICE', 'OUT OF SERVICE']
MAINTENANCE_TYPES = ['PLANNED MAINTENANCE', 'PLANNED PROACTIVE MAINTENANCE', 'REACTIVE MAINTENANCE']

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    return render_template("home.html", user=current_user)

@views.route('/assets', methods=['GET', 'POST'])
@login_required
def assets():
    if request.method == 'POST':
        AssetDescription = request.form.get('description')
        Location = request.form.get('location')
        AssetStatus = request.form.get('status')
        SerialNumber = request.form.get('serial_number')
        ClassCode = request.form.get('class_code')

        if len(AssetDescription) < MINIMUM_DESC_LENGTH:
            flash('Description is too short', category='error')
        if len(Location) < MINIMUM_DESC_LENGTH:
            flash('Location is too short', category='error')
        if AssetStatus.upper() not in ASSET_STATUSES:
            flash('Status is invalid', category='error')
        else:
            new_asset = Asset(description=AssetDescription, location=Location, status=AssetStatus,
                              serial_number=SerialNumber, class_code_id=ClassCode)
            db.session.add(new_asset)
            db.session.commit()
            flash('Asset created', category='success')

    return render_template("assets.html", user=current_user)

@views.route('/assetclassadmin', methods=['GET', 'POST'])
@login_required
def assetclassadmin():
    if request.method == 'POST':
        AssetClassCode = request.form.get('asset_class_code')
        AssetClassDesc = request.form.get('asset_class_desc')

        if len(AssetClassCode) != ASSET_CLASS_CODE_LENGTH:
            flash('Asset class code is invalid', category='error')
        elif len(AssetClassDesc) < MINIMUM_DESC_LENGTH:
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
    if request.method == 'POST':
        MaintenanceType = request.form.get('maintenance_type')
        MaintenanceDesc = request.form.get('maintenance_desc')
        AssetNumber = request.form.get('asset_id')

        if not MaintenanceType.upper() in MAINTENANCE_TYPES:
            flash('Maintenance type is invalid', category='error')
        if len(MaintenanceDesc) < MINIMUM_DESC_LENGTH:
            flash('Maintenance description is too short', category='error')
        else:
            new_maintenance = Maintenance(maintenance_type=MaintenanceType, description=MaintenanceDesc,
                                          asset_id=AssetNumber, user_id=current_user.id)
            db.session.add(new_maintenance)
            db.session.commit()
            flash('Maintenance has been successfully created', category='success')

    return render_template("maintenance.html", user=current_user)

