from flask import Flask, render_template, redirect, request
from flask_app.models.user import User
from flask_app.models.restaurant import Restaurant
from flask_app.models.menu import Menu
from flask_app.models.order import Order
from flask_app.models.order_item import OrderItem
from flask_app.models.courier import Courier
from flask_app.models.courier_application import CourierApplication
from flask_app.models.user_favorite import UserFavorite
from flask_app.models.user_past_order import UserPastOrder

app = Flask(__name__)

if __name__ == "__main__":
    app.run(debug=True)