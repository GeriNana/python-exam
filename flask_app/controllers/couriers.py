from flask import Blueprint, render_template, redirect, request, session, flash, current_app
from flask_app.models.courier import Courier
from flask_app.models.courier_application import CourierApplication
from flask_mail import Message

# Create a Blueprint named 'couriers_bp'
couriers_bp = Blueprint('couriers', __name__)

def send_application_email(applicant_data):
    # Access the mail object from the current application context
    mail = current_app.extensions['mail']
    msg = Message("New Courier Application", recipients=["your-email@gmail.com"])
    msg.body = f"""
    New Courier Application:
    Name: {applicant_data['full_name']}
    Email: {applicant_data['email']}
    Phone: {applicant_data['phone']}
    Address: {applicant_data['address']}
    City: {applicant_data['city']}
    Postal Code: {applicant_data['postal_code']}
    Vehicle Type: {applicant_data['vehicle_type']}
    """
    mail.send(msg)

@couriers_bp.route('/apply', methods=['GET', 'POST'])
def apply():
    if request.method == 'POST':
        # Collect form data
        data = {
            "full_name": request.form["full_name"],
            "email": request.form["email"],
            "phone": request.form["phone"],
            "address": request.form["address"],
            "city": request.form["city"],
            "postal_code": request.form["postal_code"],
            "vehicle_type": request.form["vehicle_type"]
        }
        # Save application to the database
        CourierApplication.save(data)
        # Send an application email
        send_application_email(data)
        # Redirect to the home page
        return redirect('/')
    # Render the application form template
    return render_template('apply.html')

@couriers_bp.route('/login', methods=['POST'])
def login():
    # Process the login form data
    email = request.form['email']
    password = request.form['password']
    # Validate login credentials
    courier = Courier.validate_login(email, password)
    if courier:
        # Set session variables
        session['courier_id'] = courier.id
        # Redirect to the home page
        return redirect('/')
    else:
        # Flash an error message
        flash("Invalid email or password", "danger")
        # Redirect back to the apply page
        return redirect('/couriers/apply')
