from flask import Blueprint, request, redirect, flash, url_for, session, render_template
from flask_app.models.favorite import Favorite
from flask_app.config.mysqlconnection import connectToMySQL

bp = Blueprint('favorites', __name__)

@bp.route('/add', methods=['POST'])
def add_favorite():
    if 'user_id' not in session:
        flash("You must be logged in to add favorites", "error")
        return redirect(url_for('users.login'))

    user_id = session['user_id']
    menu_id = request.form.get('menu_id')
    dish_id = request.form.get('dish_id')

    if not menu_id or not dish_id:
        flash("No menu item or dish specified.", "error")
        return redirect(url_for('users.user_profile', user_id=user_id))

    favorite_data = {
        "user_id": user_id,
        "menu_id": menu_id,
        "dish_id": dish_id
    }
    Favorite.add_favorite(favorite_data)
    flash("Added to favorites!", "success")
    return redirect(url_for('users.user_profile', user_id=user_id))

@bp.route('/remove', methods=['POST'])
def remove_favorite():
    if 'user_id' not in session:
        flash('You need to be logged in to remove favorites', 'error')
        return redirect(url_for('users.login'))

    data = {
        "user_id": session['user_id'],
        "menu_id": request.form.get('menu_id')
    }

    if not data['menu_id']:
        flash('No menu ID provided', 'error')
        return redirect(request.referrer)

    Favorite.remove_favorite(data)
    flash('Favorite removed successfully', 'success')
    return redirect(request.referrer)
