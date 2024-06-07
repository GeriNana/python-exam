from flask import Blueprint, render_template, redirect, request
from flask_app.models.order import Order
from flask_app.models.order_item import OrderItem
from flask_bcrypt import Bcrypt


bp = Blueprint('orders', __name__)
# Define order-related routes and logic here

def create_order():
    data = {
        "user_id": request.form["user_id"],
        "restaurant_id": request.form["restaurant_id"],
        "order_date": request.form["order_date"],
        "delivery_address": request.form["delivery_address"],
        "city": request.form["city"],
        "postal_code": request.form["postal_code"],
        "phone": request.form["phone"],
        "total_price": request.form["total_price"],
        "payment_method": request.form["payment_method"],
        "status": request.form["status"]
    }
    order_id = Order.save(data)

@bp.route('/create_order', methods=['POST'])
def create_order():
    data = {
        "user_id": request.form["user_id"],
        "restaurant_id": request.form["restaurant_id"],
        "total_price": request.form["total_price"],
        "status": request.form["status"]
    }
    Order.save(data)
    return redirect('/')

@bp.route('/order/<int:order_id>', methods=['GET'])
def get_order(order_id):
    order = Order.get_by_id(order_id)
    return render_template('order.html', order=order)