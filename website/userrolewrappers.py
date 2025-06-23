# Name: userrolewrappers
# Author: Patrick Cronin
# Date: 23/06/2025
# Updated: 23/06/2025
# Purpose: Define user role wrappers for the admin role

from functools import wraps
from flask import abort, flash, redirect, url_for
from flask_login import current_user, login_required
import logging

def admin_required(f):
    """Use this decorator to require an admin role."""
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        try:
            if not current_user.role.upper() == 'ADMIN':
                flash('You must be an administrator.', category='warning')
                abort(403)
        except AttributeError as e:
            logging.error(f"Error while checking role: {e}")
            flash('An error has occurred.', category='error')
            return redirect(url_for('auth.login'))
        except Exception as e:
            logging.error(f"Error in admin_required decorate: {e}")
            flash('An error has occurred.', category='error')
            return redirect(url_for('auth.login'))

        return f(*args, **kwargs)
    return decorated_function