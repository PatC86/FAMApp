# NAME: auth
# AUTHOR: Patrick Cronin
# Date: 22/06/2025
# Update: 22/06/2025
# Purpose: Define Authorisation Routes

from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from .models import User, Assetclass, Asset, Maintenance
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
import logging

MIN_USERNAME_LENGTH = 5
MIN_FIRST_NAME_LENGTH = 2
MIN_SURNAME_LENGTH = 2
PASSWORD_REGEX = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
ROLES = ['admin', 'user', 'facilities']

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        Username = request.form.get('username')
        Password = request.form.get('password')

        user = User.query.filter_by(username=Username).first()
        if user:
            if check_password_hash(user.password, Password):
                flash('You have been logged in.',category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password.',category='error')
        else:
            flash('Incorrect username.',category='error')


    return render_template('login.html', user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/useradmin', methods=['GET', 'POST'])
@login_required
def useradmin():
    if request.method == 'POST':
        Username = request.form.get('username')
        FirstName = request.form.get('first_name')
        Surname = request.form.get('surname')
        Role = request.form.get('role')
        Password1 = request.form.get('password1')
        Password2 = request.form.get('password2')

        if len(Username) < MIN_USERNAME_LENGTH:
            flash('Username is too short', category='error')
        elif len(FirstName) < MIN_FIRST_NAME_LENGTH:
            flash('First name is too short', category='error')
        elif len(Surname) < MIN_SURNAME_LENGTH:
            flash('Surname is too short', category='error')
        elif Password1 != Password2:
            flash('Passwords do not match', category='error')
        elif Role not in ROLES:
            flash('The role does not exist', category='error')
        else:
            new_user = User(username=Username, first_name=FirstName, surname=Surname, role=Role,
                            password=generate_password_hash(Password1, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('Account created successfully', category='success')

    return render_template('useradmin.html', user=current_user)