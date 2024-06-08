from flask import Blueprint, render_template, redirect, request, session, flash
from flask_app.models.restaurant import Restaurant

bp = Blueprint('restaurants', __name__, url_prefix='/restaurants')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        form_data = {
            "name": request.form["name"],
            "address": request.form.get("address"),
            "city": request.form.get("city"),
            "postal_code": request.form.get("postal_code"),
            "phone": request.form.get("phone"),
            "email": request.form["email"],
        }
        
        if not Restaurant.validate_registration(form_data):
            return redirect('/restaurants/register')
        
        restaurant_id = Restaurant.save(form_data)
        if restaurant_id:
            return redirect(f'/restaurants/profile/{restaurant_id}')
        else:
            return redirect('/restaurants/register')
    return render_template('register.html')

@bp.route('/profile/<int:restaurant_id>')
def restaurant_profile(restaurant_id):
    restaurant = Restaurant.get_by_id(restaurant_id)
    if not restaurant:
        return "Restaurant not found", 404
    return render_template('restaurant_profile.html', restaurant=restaurant)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = {
            "email": request.form["email"]
        }
        restaurant = Restaurant.get_by_email(data["email"])
        if not restaurant:
            flash("Invalid Email", "danger")
            return redirect('/restaurants/login')
        
        session['restaurant_id'] = restaurant.id
        return redirect(f'/restaurants/profile/{restaurant.id}')
    return render_template('login.html')

@bp.route('/logout')
def logout():
    session.pop('restaurant_id', None)
    flash("Logged out successfully.", "success")
    return redirect('/restaurants/login')

@bp.route('/search', methods=['GET'])
def search_restaurants():
    location = request.args.get('location')
    return redirect(f'/restaurants/location/{location}')

@bp.route('/location/<location>', methods=['GET'])
def show_restaurants(location):
    restaurants = Restaurant.get_by_location(location)
    return render_template('restaurants.html', location=location, restaurants=restaurants)
