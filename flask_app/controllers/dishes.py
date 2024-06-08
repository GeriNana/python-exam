from flask import Blueprint, render_template, redirect, request, flash
from flask_app.models.dish import Dish

bp = Blueprint('dishes', __name__, url_prefix='/dishes')

@bp.route('/add_dish/<int:menu_id>', methods=['GET', 'POST'])
def add_dish(menu_id):
    if request.method == 'POST':
        data = {
            "menu_id": menu_id,
            "name": request.form["name"],
            "description": request.form.get("description"),
            "price": request.form["price"],
            "image_url": request.form.get("image_url")
        }
        Dish.save(data)
        return redirect(f'/menus/view_menu/{menu_id}')
    return render_template('add_dish.html', menu_id=menu_id)

@bp.route('/edit_dish/<int:dish_id>', methods=['GET', 'POST'])
def edit_dish(dish_id):
    dish = Dish.get_by_id(dish_id)
    if not dish:
        return "Dish not found", 404
    if request.method == 'POST':
        data = {
            "id": dish_id,
            "name": request.form["name"],
            "description": request.form.get("description"),
            "price": request.form["price"],
            "image_url": request.form.get("image_url")
        }
        Dish.update(data)
        return redirect(f'/menus/view_menu/{dish.menu_id}')
    return render_template('edit_dish.html', dish=dish)

@bp.route('/delete_dish/<int:dish_id>', methods=['POST'])
def delete_dish(dish_id):
    dish = Dish.get_by_id(dish_id)
    if not dish:
        return "Dish not found", 404
    Dish.delete(dish_id)
    return redirect(f'/menus/view_menu/{dish.menu_id}')
