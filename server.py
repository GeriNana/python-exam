import os
from flask import Flask, render_template
from flask_app.controllers import users, restaurants, menus, orders, couriers
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='flask_app/templates', static_folder='flask_app/static')
app.secret_key = 'your_secret_key'  # Change this to a real secret key


@app.route('/')
def index():
    return render_template('home.html')

# Register the blueprints or controllers
app.register_blueprint(users.bp, url_prefix='/users')
app.register_blueprint(restaurants.bp, url_prefix='/restaurants')
app.register_blueprint(menus.bp, url_prefix='/menus')
app.register_blueprint(orders.bp, url_prefix='/orders')
app.register_blueprint(couriers.bp, url_prefix='/couriers')

if __name__ == "__main__":
    app.run(debug=True)
