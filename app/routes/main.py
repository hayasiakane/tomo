from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/restaurants')
def restaurant_list():
    return render_template('restaurant/restaurants.html')

@main_bp.route('/restaurants/add')
def restaurant_add():
    return render_template('restaurant/add.html')

@main_bp.route('/my-reviews')
def myreviews():
    return render_template('review/myreview.html')


@main_bp.route('/friends')
def friends_page():
    return render_template('user/friends.html')

@main_bp.route('/edit_profile')
def edit_profile_page():
    return render_template('user/edit_profile.html')

@main_bp.route('/my-restaurants')
def my_restaurants():
    return render_template('restaurant/my_restaurants.html')
