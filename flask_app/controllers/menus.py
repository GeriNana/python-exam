from flask import Blueprint, render_template, redirect, request
from flask_app.models.menu import Menu
from flask_bcrypt import Bcrypt
# Create a Blueprint for the menu routes
bp = Blueprint('menus', __name__)


def create_menu():
    data = {
        "restaurant_id": request.form["restaurant_id"],
        "name": request.form["name"],
        "description": request.form["description"],
        "price": request.form["price"],
        "image_url": request.form["image_url"]
    }
    Menu.save(data)
    return redirect('/')


# Define your routes using the Blueprint object
@bp.route('/create_menu', methods=['POST'])
def create_menu():
    data = {
        "restaurant_id": request.form["restaurant_id"],
        "name": request.form["name"],
        "description": request.form["description"],
        "price": request.form["price"]
    }
    Menu.save(data)
    return redirect('/')

@bp.route('/menus/<int:menu_id>', methods=['GET'])
def get_menu(menu_id):
    menu = Menu.get_by_id(menu_id)
    return render_template('menu.html', menu=menu)
