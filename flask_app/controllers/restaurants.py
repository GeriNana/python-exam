from flask import Blueprint, render_template, redirect, request, session, flash, url_for
from flask_app.models.menu import Menu
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
    return redirect(url_for('restaurants.show_restaurants', location=location))

@bp.route('/location/<string:location>')
def show_restaurants(location):
    restaurants = Restaurant.get_by_location(location)
    for restaurant in restaurants:
        restaurant.menus = Menu.get_by_restaurant_id(restaurant.id)
    return render_template('restaurants.html', location=location, restaurants=restaurants)

@bp.route('/menu/<int:menu_id>')
def show_menu(menu_id):
    menu = Menu.get_by_id(menu_id)
    if not menu:
        return "Menu not found", 404
    return render_template('show_menu.html', menu=menu)


@bp.route('/edit_profile/<int:restaurant_id>', methods=['GET', 'POST'])
def edit_profile(restaurant_id):
    if 'user_id' not in session:
        flash('You need to be logged in to access this page.')
        return redirect(url_for('users.login'))
    
    restaurant = Restaurant.get_by_id(restaurant_id)
    if not restaurant:
        flash('Restaurant not found.')
        return redirect(url_for('restaurants.profile', restaurant_id=restaurant_id))
    
    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        city = request.form['city']
        postal_code = request.form['postal_code']
        phone = request.form['phone']
        email = request.form['email']

        if email != restaurant.email and Restaurant.get_by_email(email):
            flash('Email is already in use.')
            return redirect(url_for('restaurants.edit_profile', restaurant_id=restaurant_id))

        data = {
            'id': restaurant_id,
            'name': name,
            'address': address,
            'city': city,
            'postal_code': postal_code,
            'phone': phone,
            'email': email
        }
        Restaurant.update(data)
        flash('Profile updated successfully.')
        return redirect(url_for('restaurants.restaurant_profile', restaurant_id=restaurant_id))
    
    return render_template('edit_profile.html', restaurant=restaurant)
@bp.route('/delete_account/<int:restaurant_id>', methods=['POST'])
def delete_account(restaurant_id):
    Restaurant.delete(restaurant_id)
    flash("Account deleted successfully.", "success")
    return redirect(url_for('index'))