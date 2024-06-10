from flask import Blueprint, request, jsonify, session, redirect, render_template
from flask_app.models.favorite import Favorite

bp = Blueprint('favorites', __name__, url_prefix='/favorites')

@bp.route('/add', methods=['POST'])
def add_favorite():
    if 'user_id' not in session:
        return jsonify({"success": False, "message": "You need to be logged in to add favorites."})
    
    data = request.get_json()
    user_id = session['user_id']
    dish_id = data['dish_id']
    
    favorite_data = {
        'user_id': user_id,
        'dish_id': dish_id
    }
    
    if Favorite.save(favorite_data):
        return jsonify({"success": True})
    else:
        return jsonify({"success": False, "message": "Failed to add favorite."})

@bp.route('/<int:user_id>', methods=['GET'])
def get_favorites(user_id):
    if 'user_id' not in session:
        return redirect('/users/login')
    
    if session['user_id'] != user_id:
        return redirect('/')
    
    favorites = Favorite.get_by_user_id(user_id)
    return render_template('favorites.html', favorites=favorites)
