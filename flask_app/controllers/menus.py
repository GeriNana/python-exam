from flask import Blueprint, render_template, redirect, request, session, flash
from flask_app.models.menu import Menu

bp = Blueprint('menus', __name__, url_prefix='/menus')

@bp.route('/add/<int:restaurant_id>', methods=['GET', 'POST'])
def add_menu(restaurant_id):
    if request.method == 'POST':
        data = {
            "restaurant_id": restaurant_id,
            "name": request.form["name"],
            "description": request.form.get("description"),
            "price": request.form["price"],
            "image_url": request.form.get("image_url")
        }
        Menu.save(data)
        return redirect(f'/restaurants/profile/{restaurant_id}')
    return render_template('add_menu.html', restaurant_id=restaurant_id)
