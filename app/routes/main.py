from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/restaurants')
def restaurant_list():
    return render_template('restaurant/restaurants.html')

@main_bp.route('/restaurants/<restaurant_id>')
def restaurant_detail(restaurant_id):
    return render_template('restaurant/detail.html', restaurant_id=restaurant_id)

@main_bp.route('/restaurants/add')
def restaurant_add():
    return render_template('restaurant/add.html')

@main_bp.route('/my-reviews')
def myreviews():
    return render_template('review/myreview.html')