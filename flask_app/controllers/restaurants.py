from flask import Blueprint, render_template, request, redirect
from flask_app.models.restaurant import Restaurant

bp = Blueprint('restaurants', __name__)

@bp.route('/add', methods=['GET', 'POST'])
def create_restaurant():
    if request.method == 'POST':
        data = {
            "name": request.form["name"],
            "address": request.form["address"],
            "city": request.form["city"],
            "postal_code": request.form["postal_code"],
            "phone": request.form["phone"],
            "email": request.form["email"],
            "logo_url": request.form["logo_url"]
        }
        Restaurant.save(data)
        return redirect('/')
    return render_template('add_restaurant.html')

@bp.route('/search', methods=['GET'])
def search_restaurants():
    location = request.args.get('location')
    return redirect(f'/restaurants/{location}')

@bp.route('/<location>', methods=['GET'])
def show_restaurants(location):
    restaurants = Restaurant.get_by_location(location)
    return render_template('restaurants.html', location=location, restaurants=restaurants)
