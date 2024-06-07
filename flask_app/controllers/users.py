from flask import Blueprint, render_template, redirect, request, session, flash
from flask_app.models.user import User
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
bp = Blueprint('users', __name__)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = {
            "username": request.form["username"],
            "email": request.form["email"],
            "password": request.form["password"],
            "full_name": request.form.get("full_name"),
            "address": request.form.get("address"),
            "city": request.form.get("city"),
            "postal_code": request.form.get("postal_code"),
            "phone": request.form.get("phone"),
            "preferred_payment_method": request.form.get("preferred_payment_method")
        }

        if not User.validate_registration(data):
            return redirect('/register')

        data['password'] = bcrypt.generate_password_hash(data['password'])
        user_id = User.save(data)
        session['user_id'] = user_id
        return redirect('/')
    return render_template('register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = {
            "email": request.form["email"],
            "password": request.form["password"]
        }
        user = User.get_by_email(data['email'])
        if not user or not bcrypt.check_password_hash(user.password, data['password']):
            flash("Invalid Email/Password")
            return redirect('/login')
        session['user_id'] = user.id
        return redirect('/')
    return render_template('login.html')
