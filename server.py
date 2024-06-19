import os
from flask import Flask, render_template, redirect, request, url_for, session, jsonify
from flask_mail import Mail, Message
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.controllers import users, restaurants, menus, dishes, favorites
from flask_app.controllers.orders import orders_bp
from flask_app.controllers.couriers import couriers_bp  # Ensure this is correctly imported
import paypalrestsdk
import requests

app = Flask(__name__, template_folder='flask_app/templates', static_folder='flask_app/static')
app.secret_key = 'your_secret_key'  # Change this to a real secret key

# Email Configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'gastroglide.albania@gmail.com'
app.config['MAIL_PASSWORD'] = 'blummen2024'
mail = Mail(app)  # This initializes your Mail object

paypalrestsdk.configure({
    "mode": "sandbox",  # sandbox or live
    "client_id": "YOUR_PAYPAL_CLIENT_ID",
    "client_secret": "YOUR_PAYPAL_CLIENT_SECRET"
})
@app.route('/')
def index():
    return render_template('home.html')  # Ensure 'home.html' exists in your templates directory

# Blueprint registration
app.register_blueprint(users.bp, url_prefix='/users')
app.register_blueprint(restaurants.bp, url_prefix='/restaurants')
app.register_blueprint(menus.bp, url_prefix='/menus')
app.register_blueprint(orders_bp, url_prefix='/orders')
app.register_blueprint(favorites.bp, url_prefix='/favorites')
app.register_blueprint(couriers_bp, url_prefix='/couriers')  # Correctly reference the Blueprint
app.register_blueprint(dishes.bp, url_prefix='/dishes')

if __name__ == "__main__":
    app.run(debug=True)
