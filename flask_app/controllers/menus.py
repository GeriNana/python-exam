from flask import Blueprint, render_template, redirect, request, session, flash
from flask_app.models.menu import Menu

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
    menu = Menu.get_by_id(menu_id)
    if not menu:
        return "Menu not found", 404
    Menu.delete(menu_id)
    return redirect(f'/restaurants/profile/{menu.restaurant_id}')
