from flask import Blueprint, render_template, redirect, request, session, flash
from flask_app.models.user import User

bp = Blueprint('users', __name__, url_prefix='/users')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = {
            "username": request.form["username"],
            "full_name": request.form["full_name"],
            "address": request.form["address"],
            "city": request.form["city"],
            "postal_code": request.form["postal_code"],
            "phone": request.form["phone"],
            "email": request.form["email"],
            "password": request.form["password"]
        }
        if not User.validate_registration(data):
            return redirect('/users/register')
        user_id = User.save(data)
        session['user_id'] = user_id
        return redirect(f'/users/profile/{user_id}')
    return render_template('register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = {
            "email": request.form["email"],
            "password": request.form["password"]
        }
        user = User.get_by_email(data["email"])
        print("User found:", user)  # Add this line to see what user object is created
        if not user or not User.check_password(user.password, data["password"]):
            flash("Invalid Email/Password", "danger")
            return redirect('/users/login')
        
        session['user_id'] = user.id
        return redirect(f'/users/profile/{user.id}')
    return render_template('login.html')

@bp.route('/profile/<int:user_id>')
def user_profile(user_id):
    if 'user_id' not in session or session['user_id'] != user_id:
        return redirect('/users/login')
    user = User.get_by_id(user_id)
    return render_template('profile.html', user=user)

@bp.route('/logout')
def logout():
    session.clear()
    return redirect('/')
