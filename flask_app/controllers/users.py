from flask import Blueprint, request, redirect, flash, url_for, render_template, session
from flask_app.models.user import User
from flask_app.models.order import Order
from flask_app.models.order_item import OrderItem
from flask_app.models.menu import Menu
from flask_app.models.favorite import Favorite
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
bp = Blueprint('users', __name__, url_prefix='/users')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        form_data = request.form.to_dict()
        username = form_data.get("username")
        full_name = form_data.get("full_name")
        email = form_data.get("email")
        password = form_data.get("password")
        
        if not all([username, full_name, email, password]):
            flash("All fields are required!", "error")
            return redirect(url_for('users.register'))
        
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user_data = {
            "username": username,
            "full_name": full_name,
            "email": email,
            "password": hashed_password
        }
        
        if User.validate_registration(user_data):
            user_id = User.save(user_data)
            if user_id:
                flash("Registration successful!", "success")
                session['user_id'] = user_id
                return redirect(url_for('users.profile', user_id=user_id))
            else:
                flash("Registration failed. Please try again.", "error")
                return redirect(url_for('users.register'))
        else:
            return redirect(url_for('users.register'))
    return render_template('register.html')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.get_by_email(email)
        if user:
            try:
                if bcrypt.check_password_hash(user.password, password):
                    session['user_id'] = user.id
                    flash('Login successful!', 'success')
                    return redirect(url_for('users.profile', user_id=user.id))
                else:
                    flash('Invalid email or password', 'error')
            except ValueError:
                flash('Invalid email or password', 'error')
        else:
            flash('Invalid email or password', 'error')
        return redirect(url_for('users.login'))
    return render_template('login.html')

@bp.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))

@bp.route('/profile/<int:user_id>')
def profile(user_id):
    if 'user_id' not in session:
        return redirect(url_for('users.login'))
    
    if session['user_id'] != user_id:
        flash('You do not have permission to view this profile.', 'error')
        return redirect(url_for('index'))
    
    user = User.get_by_id(user_id)
    if not user:
        flash('User not found', 'error')
        return redirect(url_for('index'))
    
    user.past_orders = Order.get_by_user_id(user_id)
    user.favorites = Favorite.get_by_user_id(user_id)
    
    print(f"Past orders for user {user_id}: {user.past_orders}")
    print(f"Favorites for user {user_id}: {user.favorites}")
    
    return render_template('profile.html', user=user)


@bp.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if 'user_id' not in session:
        flash('You need to be logged in to checkout', 'error')
        return redirect(url_for('users.login'))
    
    if request.method == 'POST':
        user_id = session['user_id']
        basket = request.get_json()

        # Create a new order
        order_data = {
            'user_id': user_id,
            'total_price': sum(item['price'] * item['quantity'] for item in basket.values()),
            'status': 'Pending'
        }
        order_id = Order.save(order_data)

        # Create order items
        for dish_name, item in basket.items():
            menu_item = Menu.get_by_name(dish_name)  # Assuming you have a method to get a menu item by name
            if menu_item:
                order_item_data = {
                    'order_id': order_id,
                    'menu_id': menu_item.id,
                    'quantity': item['quantity'],
                    'price': item['price']
                }
                OrderItem.save(order_item_data)

        flash('Order placed successfully', 'success')
        return redirect(url_for('orders.confirmation', order_id=order_id))
    
    return render_template('checkout.html')
