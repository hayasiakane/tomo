from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.user import User
from app.utils.decorators import login_required
from werkzeug.security import generate_password_hash
from gremlin_python.driver import client
import uuid
import datetime
user_bp = Blueprint('user', __name__)

@user_bp.route('/profile/<userid>')
@login_required
def profile():
    user_id = request.cookies.get('user_id')
    user, error = User.get_by_id(user_id)
    if error:
        flash(error, 'danger')
        return redirect(url_for('main.index'))
    
    return render_template('user/profile.html', user=user)

@user_bp.route('/friends')
@login_required
def friends():
    user_id = request.cookies.get('user_id')
    friends, error = User.get_friends(user_id)
    if error:
        flash(error, 'danger')
        return redirect(url_for('main.index'))
    
    return render_template('user/friends.html', friends=friends) #friends.html未生成

