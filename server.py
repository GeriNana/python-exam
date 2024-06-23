import os
from flask import Flask, render_template, redirect, request, url_for, session, jsonify
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.controllers import users, restaurants, menus, dishes, favorites, couriers
from flask_app.controllers.orders import orders_bp
from flask_app.controllers.couriers import couriers_bp 
import paypalrestsdk
import requests
from settings import Settings
import logging
from flask_bcrypt import Bcrypt
import json
app = Flask(__name__, template_folder='flask_app/templates', static_folder='flask_app/static')
bcrypt = Bcrypt(app)

app.config.from_object('settings.Settings')

mail = Mail(app)

logging.basicConfig(level=logging.DEBUG)

@app.route('/index')
def index():
    return redirect(url_for('home'))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/language/<lang>', methods=['GET'])
def get_language(lang):
    try:
        with open(f'translations/{lang}.json', 'r', encoding='utf-8') as f:
            translations = json.load(f)
        return jsonify(translations)
    except FileNotFoundError:
        return jsonify({"error": "Language file not found"}), 404



# Set bcrypt attribute in couriers blueprint
couriers.bcrypt = bcrypt

# Blueprint registration
app.register_blueprint(users.bp, url_prefix='/users')
app.register_blueprint(restaurants.bp, url_prefix='/restaurants')
app.register_blueprint(menus.bp, url_prefix='/menus')
app.register_blueprint(orders_bp, url_prefix='/orders')
app.register_blueprint(favorites.bp, url_prefix='/favorites')
app.register_blueprint(couriers_bp, url_prefix='/couriers') 
app.register_blueprint(dishes.bp, url_prefix='/dishes')

if __name__ == "__main__":
    app.run(debug=True)
