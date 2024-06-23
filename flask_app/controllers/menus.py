from flask import Blueprint, render_template, redirect, request, session, flash, url_for
from flask_app.models.menu import Menu
from flask_app.models.dish import Dish
from flask_app.models.restaurant import Restaurant
from flask_app.models.order_item import OrderItem
from flask_app.models.favorite import Favorite

bp = Blueprint('menus', __name__, url_prefix='/menus')

@bp.route('/add_menu/<int:restaurant_id>', methods=['GET', 'POST'])
def add_menu(restaurant_id):
    if request.method == 'POST':
        data = {
            "restaurant_id": restaurant_id,
            "image_url": request.form.get("image_url"),
            "restaurant_name": request.form["restaurant_name"],
            "min_order_amount": request.form["min_order_amount"],
            "avg_preparation_time": request.form["avg_preparation_time"]
        }
        Menu.save(data)
        return redirect(f'/restaurants/profile/{restaurant_id}')
    return render_template('add_menu.html', restaurant_id=restaurant_id)

@bp.route('/view_menu/<int:menu_id>')
def view_menu(menu_id):
    menu = Menu.get_by_id(menu_id)
    if not menu:
        return "Menu not found", 404
    return render_template('view_menu.html', menu=menu)

@bp.route('/show_menu/<int:menu_id>')
def show_menu(menu_id):
    menu = Menu.get_by_id(menu_id)
    dishes = Dish.get_by_menu_id(menu_id)

    basket = []
    total_price = 0.0

    if 'order_id' in session:
        order_id = session['order_id']
        order_items = OrderItem.get_by_order_id(order_id)
        for item in order_items:
            dish = Dish.get_by_id(item.dish_id)
            basket.append({
                'dish_name': dish.name,
                'price': float(item.price),  # Ensure price is float
                'quantity': item.quantity
            })
            total_price += float(item.price) * item.quantity

    return render_template('show_menu.html', menu=menu, dishes=dishes, basket=basket, total_price=total_price)

@bp.route('/edit_menu/<int:menu_id>', methods=['GET', 'POST'])
def edit_menu(menu_id):
    menu = Menu.get_by_id(menu_id)
    if not menu:
        return "Menu not found", 404
    if request.method == 'POST':
        data = {
            "id": menu_id,
            "image_url": request.form.get("image_url"),
            "restaurant_name": request.form["restaurant_name"],
            "min_order_amount": request.form["min_order_amount"],
            "avg_preparation_time": request.form["avg_preparation_time"]
        }
        Menu.update(data)
        return redirect(f'/menus/view_menu/{menu_id}')
    return render_template('edit_menu.html', menu=menu)

@bp.route('/delete_menu/<int:menu_id>', methods=['POST'])
def delete_menu(menu_id):
    try:
        # Debug statement to print the form data
        print("Form data:", request.form)
        
        # Get all dishes related to the menu
        dishes = Dish.get_by_menu_id(menu_id)
        
        # Delete all related order items and user favorites
        for dish in dishes:
            OrderItem.delete_by_dish_id(dish.id)
            Favorite.delete_by_dish_id(dish.id)
        
        # Delete all dishes related to the menu
        for dish in dishes:
            Dish.delete(dish.id)
        
        # Delete the menu
        Menu.delete(menu_id)
        flash('Menu and all related dishes deleted successfully.', 'success')
    except Exception as e:
        flash(f'Something went wrong: {e}', 'error')

    return redirect(url_for('restaurants.profile', restaurant_id=request.form['restaurant_id']))
