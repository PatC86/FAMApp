# NAME: views
# AUTHOR: Patrick Cronin
# Date: 22/06/2025
# Update: 24/06/2025
# Purpose: Define views/routes for the application

from .models import Assetclass, Asset, Maintenance, User
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from . import db
from .userrolewrappers import admin_required
from .auth import ROLES, useradmin

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

    AssetList = db.session.query(Asset, Assetclass).join(Assetclass, Asset.class_code_id == Assetclass.class_code).all()
    return render_template("assets.html", user=current_user, asset_list=AssetList)

@views.route('/assetclassadmin', methods=['GET', 'POST'])
@admin_required
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

    AssetClassList = db.session.query(Assetclass).all()
    return render_template("assetclassadmin.html", user=current_user, asset_class_list=AssetClassList)

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
    MaintenanceList = db.session.query(Maintenance, Asset, Assetclass).join(Asset, Maintenance.asset_id == Asset.id).join(Assetclass, Asset.class_code_id == Assetclass.class_code).all()
    return render_template("maintenance.html", user=current_user, maintenance_list=MaintenanceList)

@views.route('/update_role/<int:id>', methods=['POST'])
@admin_required
def update_role(id):

    NewRole = request.form.get('role')
    if NewRole not in ROLES:
        flash('Role does not exist', category='error')

    changinguser = User.query.get(id)
    if changinguser:
        changinguser.role = NewRole
        db.session.commit()
        flash('Role has been successfully updated', category='success')
    else:
        flash('User not found', category='error')
    UserList = db.session.query(User.id, User.username, User.first_name, User.surname, User.role).all()
    return render_template('useradmin.html', user=current_user, user_list=UserList)

@views.route('/delete_user/<int:id>', methods=['POST'])
@admin_required
def delete_user(id):

    DeleteUser = User.query.get(id)
    if DeleteUser:
        db.session.delete(DeleteUser)
        db.session.commit()
        flash('User has been successfully deleted', category='success')
    else:
        flash('Error user not found', category='error')

    UserList = db.session.query(User.id, User.username, User.first_name, User.surname, User.role).all()
    return render_template('useradmin.html', user=current_user, user_list=UserList)

@views.route('/delete_asset_class/<class_code>', methods=['POST'])
@admin_required
def delete_asset_class(class_code):
    DeleteAssetClass = Assetclass.query.get(class_code)
    if DeleteAssetClass:
        db.session.delete(DeleteAssetClass)
        db.session.commit()
        flash('Asset class has been successfully deleted', category='success')
    else:
        flash('Asset class not found', category='error')

    AssetClassList = db.session.query(Assetclass).all()
    return render_template('assetclassadmin.html', user=current_user, asset_class_list=AssetClassList)

@views.route('/delete_asset/<int:id>', methods=['POST'])
@login_required
def delete_asset(id):
    DeleteAsset = Asset.query.get(id)
    if DeleteAsset:
        db.session.delete(DeleteAsset)
        db.session.commit()
        flash('Asset has been successfully deleted', category='success')
    else:
        flash('Asset not found', category='error')
    AssetList = db.session.query(Asset, Assetclass).join(Assetclass, Asset.class_code_id == Assetclass.class_code).all()
    return render_template('assets.html', user=current_user, asset_list=AssetList)

@views.route('/delete_maintenance/<int:id>', methods=['POST'])
@login_required
def delete_maintenance(id):
    DeleteMaintenance = Maintenance.query.get(id)
    if DeleteMaintenance:
        db.session.delete(DeleteMaintenance)
        db.session.commit()
        flash('Maintenance has been successfully deleted', category='success')
    else:
        flash('Maintenance not found', category='error')
    MaintenanceList = db.session.query(Maintenance, Asset, Assetclass).join(Asset,
                                                                            Maintenance.asset_id == Asset.id).join(
        Assetclass, Asset.class_code_id == Assetclass.class_code).all()
    return render_template("maintenance.html", user=current_user, maintenance_list=MaintenanceList)

@views.route('/edit_asset_class/<class_code>', methods=['POST'])
@admin_required
def edit_asset_class(class_code):
    NewData = request.get_json()
    print("Received new data:", NewData)
    print("Class code:", class_code)

    EditAssetClass = Assetclass.query.get(class_code)

    if EditAssetClass:
        EditAssetClass.class_desc = NewData['asset_class_desc']
        db.session.commit()
        print("Asset class description:", EditAssetClass.class_desc)
        flash('Asset class description has been successfully updated', category='success')
    else:
        flash('Asset class not found', category='error')

    AssetClassList = db.session.query(Assetclass).all()
    return render_template('assetclassadmin.html', user=current_user, asset_class_list=AssetClassList)



