from flask import Blueprint, render_template, redirect, request, session, flash, current_app, url_for
from flask_app.models.courier import Courier
from flask_app.models.courier_application import CourierApplication
from flask_mail import Message

couriers_bp = Blueprint('couriers', __name__)

# This will be set from the main application file
bcrypt = None

def send_confirmation_email(email, token):
    mail = current_app.extensions['mail']
    confirm_url = url_for('couriers.confirm_email', token=token, _external=True)
    html = render_template('activate.html', confirm_url=confirm_url)
    msg = Message("Please confirm your email", recipients=[email])
    msg.html = html
    mail.send(msg)

def send_application_email(applicant_data, token):
    mail = current_app.extensions['mail']
    confirm_url = url_for('couriers.confirm_email', token=token, _external=True)
    msg = Message("New Courier Application", recipients=["gastroglide.albania@gmail.com"])
    msg.body = f"""
    New Courier Application:
    Name: {applicant_data['full_name']}
    Email: {applicant_data['email']}
    Phone: {applicant_data['phone']}
    Address: {applicant_data['address']}
    City: {applicant_data['city']}
    Postal Code: {applicant_data['postal_code']}
    Vehicle Type: {applicant_data['vehicle_type']}

    Activate Account Link: {confirm_url}
    """
    mail.send(msg)

@couriers_bp.route('/apply', methods=['GET', 'POST'])
def apply():
    if request.method == 'POST':
        data = {
            "full_name": request.form["full_name"],
            "email": request.form["email"],
            "phone": request.form["phone"],
            "address": request.form["address"],
            "city": request.form["city"],
            "postal_code": request.form["postal_code"],
            "vehicle_type": request.form["vehicle_type"]
        }
        CourierApplication.save(data)
        token = CourierApplication.generate_confirmation_token(data['email'])
        send_confirmation_email(data['email'], token)
        send_application_email(data, token)
        flash('A confirmation email has been sent via email.', 'success')
        return redirect('/')
    return render_template('apply.html')

@couriers_bp.route('/confirm/<token>', methods=['GET', 'POST'])
def confirm_email(token):
    try:
        email = CourierApplication.confirm_token(token)
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')
        return redirect('/')
    
    courier_application = CourierApplication.get_by_email(email)
    if not courier_application:
        flash('Application not found.', 'danger')
        return redirect('/')
    
    if request.method == 'POST':
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        courier_data = {
            "full_name": courier_application.full_name,
            "email": courier_application.email,
            "phone": courier_application.phone,
            "address": courier_application.address,
            "city": courier_application.city,
            "postal_code": courier_application.postal_code,
            "vehicle_type": courier_application.vehicle_type,
            "password": hashed_password,
            "confirmed": 1
        }
        Courier.save(courier_data)
        flash('You have confirmed your account. You can now log in!', 'success')
        return redirect('/couriers/login')
    
    return render_template('set_password.html')

@couriers_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        courier = Courier.get_by_email(email)
        
        if courier and bcrypt.check_password_hash(courier.password, password):
            if courier.confirmed:
                session['courier_id'] = courier.id
                flash('Login successful!', 'success')
                return redirect(url_for('couriers.profile'))
            else:
                flash('Please confirm your email first.', 'warning')
        else:
            flash('Invalid email or password.', 'danger')
    
    return render_template('couriers_login.html')

@couriers_bp.route('/profile')
def profile():
    if 'courier_id' not in session:
        flash('Please log in to view this page.', 'danger')
        return redirect(url_for('couriers.login'))
    
    courier = Courier.get_by_id(session['courier_id'])
    return render_template('courier_profile.html', courier=courier)

@couriers_bp.route('/profile/edit', methods=['GET', 'POST'])
def edit_profile():
    if 'courier_id' not in session:
        flash('Please log in to view this page.', 'danger')
        return redirect(url_for('couriers.login'))
    
    courier = Courier.get_by_id(session['courier_id'])

    if request.method == 'POST':
        courier_data = {
            "id": courier.id,
            "full_name": request.form['full_name'],
            "email": request.form['email'],
            "phone": request.form['phone'],
            "address": request.form['address'],
            "city": request.form['city'],
            "postal_code": request.form['postal_code'],
            "vehicle_type": request.form['vehicle_type'],
            "password": courier.password,
            "confirmed": courier.confirmed
        }
        Courier.update(courier_data)
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('couriers.profile'))
    
    return render_template('edit_courier_profile.html', courier=courier)

@couriers_bp.route('/profile/delete', methods=['POST'])
def delete_profile():
    if 'courier_id' not in session:
        flash('Please log in to view this page.', 'danger')
        return redirect(url_for('couriers.login'))
    
    Courier.delete(session['courier_id'])
    session.pop('courier_id', None)
    flash('Profile deleted successfully!', 'success')
    return redirect(url_for('couriers.login'))

@couriers_bp.route('/home')
def home():
    if 'courier_id' not in session:
        return redirect(url_for('couriers.login'))
    return render_template('home.html')

@couriers_bp.route('/logout')
def logout():
    session.pop('courier_id', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('couriers.login'))

@couriers_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        full_name = request.form['full_name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        city = request.form['city']
        postal_code = request.form['postal_code']
        vehicle_type = request.form['vehicle_type']
        password = request.form['password']
        
        # Hash the password
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        
        # Create courier data dictionary
        courier_data = {
            "full_name": full_name,
            "email": email,
            "phone": phone,
            "address": address,
            "city": city,
            "postal_code": postal_code,
            "vehicle_type": vehicle_type,
            "password": hashed_password,
            "confirmed": 0  # Set to 0 initially
        }
        
        # Save courier to database
        Courier.save(courier_data)
        
        # Generate confirmation token and send email
        token = CourierApplication.generate_confirmation_token(email)
        send_confirmation_email(email, token)
        
        flash('A confirmation email has been sent via email.', 'success')
        return redirect('/')
    return render_template('apply.html')
