from flask_app import app
from flask import render_template, redirect, session, request, flash
from flask_bcrypt import Bcrypt
from flask_app.models.user import User

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    print(f"Session data at index: {session}")
    if 'user_id' in session:
        print("User is logged in, redirecting to dashboard")
        return redirect('/dashboard')
    print("User is not logged in, showing loginRegister page")
    return render_template('loginRegister.html')

@app.route('/register')
def registerPage():
    if 'user_id' in session:
        return redirect('/dashboard')
    return render_template('loginRegister.html')

@app.route('/register', methods=['POST'])
def register():
    if 'user_id' in session:
        return redirect('/dashboard')
    if not User.validate_userRegister(request.form):
        return redirect(request.referrer)
    user = User.get_user_by_email(request.form)
    if user:
        flash('This account already exists', 'emailRegister')
        return redirect(request.referrer)
    data = {
        'first_name': request.form.get('first_name'),
        'last_name': request.form.get('last_name'),
        'email': request.form.get('email'),
        'password': bcrypt.generate_password_hash(request.form.get('password')).decode('utf-8')
    }
    user_id = User.create(data)
    if not user_id:
        flash('An error occurred. Please try again.', 'registerError')
        return redirect(request.referrer)
    session['user_id'] = user_id
    return redirect('/dashboard')

@app.route('/login')
def loginPage():
    if 'user_id' in session:
        return redirect('/dashboard')
    return render_template('loginRegister.html')

@app.route('/login', methods=['POST'])
def login():
    if 'user_id' in session:
        return redirect('/')
    
    email = request.form.get('email')
    password = request.form.get('password')
    
    if not email:
        flash('Email is required', 'emailLogin')
        return redirect(request.referrer)
    
    if not password:
        flash('Password is required', 'passwordLogin')
        return redirect(request.referrer)
    
    user = User.get_user_by_email({'email': email})
    if not user:
        flash('This user is not registered yet', 'emailLogin')
        return redirect(request.referrer)
    
    if not bcrypt.check_password_hash(user.password, password):
        flash('Incorrect password', 'passwordLogin')
        return redirect(request.referrer)
    
    session['user_id'] = user.id
    return redirect('/dashboard')

@app.route('/logout')
def logout():
    print(f"Logging out, session before clear: {session}")
    session.clear()
    print(f"Session after clear: {session}")
    return redirect('/')

