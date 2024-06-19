from flask import Blueprint, request, render_template, redirect, url_for, session, flash, jsonify
from flask_app.config.mysqlconnection import connectToMySQL
import requests
from flask_bcrypt import Bcrypt
from flask_app.models.user import User
from flask_app.order_utils import insert_order, get_past_orders, calculate_total_price
from flask_app.models.user import get_user_by_id

orders_bp = Blueprint('orders', __name__)

def process_paypal_payment(total):
    client_id = 'YOUR_PAYPAL_CLIENT_ID'
    secret = 'YOUR_PAYPAL_SECRET'
    paypal_api_url = 'https://api.sandbox.paypal.com/v1/oauth2/token'
    payment_url = 'https://api.sandbox.paypal.com/v1/payments/payment'

    auth_response = requests.post(
        paypal_api_url,
        headers={'Accept': 'application/json', 'Accept-Language': 'en_US'},
        auth=(client_id, secret),
        data={'grant_type': 'client_credentials'}
    )

    if auth_response.status_code != 200:
        return {"success": False}

    auth_data = auth_response.json()
    access_token = auth_data['access_token']

    payment_data = {
        "intent": "sale",
        "payer": {"payment_method": "paypal"},
        "transactions": [{
            "amount": {"total": total, "currency": "USD"},
            "description": "Your order description"
        }],
        "redirect_urls": {
            "return_url": "http://localhost:5000/orders/paypal/complete",
            "cancel_url": "http://localhost:5000/orders/paypal/cancel"
        }
    }

    payment_response = requests.post(
        payment_url,
        headers={'Content-Type': 'application/json', 'Authorization': f'Bearer {access_token}'},
        json=payment_data
    )

    if payment_response.status_code != 201:
        return {"success": False}

    payment_data = payment_response.json()
    approval_url = next(link['href'] for link in payment_data['links'] if link['rel'] == 'approval_url')

    return {"success": True, "approval_url": approval_url}

@orders_bp.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if 'user_id' in session:
        user_id = session['user_id']
        user_data = get_user_by_id(user_id)
        if request.method == 'POST':
            restaurant_id = request.form['restaurant_id']
            order_id = request.form['order_id']
            total_price = calculate_total_price(order_id)
            if total_price is None:
                flash('Could not calculate total price.', 'danger')
                return redirect(url_for('orders.checkout'))

            payment_method = request.form['payment_method']
            address = user_data.address
            postal_code = user_data.postal_code
            phone = user_data.phone

            order_id = insert_order(user_id, total_price, address, postal_code, phone, payment_method, restaurant_id)
            flash('Order placed successfully!', 'success')
            return redirect(url_for('orders.delivery_status', order_id=order_id))
        
        order_id = ...  # Fetch or generate order ID
        restaurant_id = ...  # Fetch or generate restaurant ID
        total_price = calculate_total_price(order_id)
        if total_price is None:
            total_price = 0.0  # Default to 0.0 or handle appropriately

        return render_template('checkout.html', user_logged_in=True, user_address=user_data.address,
                               user_postal_code=user_data.postal_code, user_phone=user_data.phone,
                               total_price=total_price, order_id=order_id, restaurant_id=restaurant_id)
    else:
        if request.method == 'POST':
            restaurant_id = request.form['restaurant_id']
            order_id = request.form['order_id']
            total_price = calculate_total_price(order_id)
            if total_price is None:
                flash('Could not calculate total price.', 'danger')
                return redirect(url_for('orders.checkout'))

            payment_method = request.form['payment_method']
            address = request.form['address']
            postal_code = request.form['postal_code']
            phone = request.form['phone']

            order_id = insert_order(None, total_price, address, postal_code, phone, payment_method, restaurant_id)
            flash('Order placed successfully!', 'success')
            return redirect(url_for('orders.delivery_status', order_id=order_id))

        order_id = ...  # Fetch or generate order ID
        restaurant_id = ...  # Fetch or generate restaurant ID
        total_price = calculate_total_price(order_id)
        if total_price is None:
            total_price = 0.0  # Default to 0.0 or handle appropriately

        return render_template('checkout.html', user_logged_in=False, total_price=total_price, order_id=order_id, restaurant_id=restaurant_id)

@orders_bp.route('/complete_checkout', methods=['POST'])
def complete_checkout():
    try:
        total_price = float(request.form['total_price'])
    except ValueError:
        flash('Invalid total price.', 'danger')
        return redirect(url_for('orders.checkout'))

    payment_method = request.form['payment_method']
    restaurant_id = request.form.get('restaurant_id')
    if not restaurant_id:
        flash('Restaurant ID is required.', 'danger')
        return redirect(url_for('orders.checkout'))

    if 'user_id' in session:
        user_id = session['user_id']
        user_data = get_user_by_id(user_id)
        address = user_data.address
        postal_code = user_data.postal_code
        phone = user_data.phone
    else:
        address = request.form['address']
        postal_code = request.form['postal_code']
        phone = request.form['phone']
        user_id = None  # Handle anonymous user

    order_id = insert_order(user_id, total_price, address, postal_code, phone, payment_method, restaurant_id)
    flash('Order placed successfully!', 'success')
    return render_template('delivery_status.html', delivery_address=address)

    order_id = insert_order(user_id, total_price, address, postal_code, phone, payment_method, restaurant_id)
    flash('Order placed successfully!', 'success')
    return render_template('delivery_status.html', delivery_address=address)

@orders_bp.route('/delivery_status')
def delivery_status():
    return render_template('delivery_status.html')

@orders_bp.route('/past_orders/<int:user_id>')
def past_orders(user_id):
    orders = get_past_orders(user_id)
    return render_template('past_orders.html', orders=orders)

@orders_bp.route('/paypal/complete', methods=['GET', 'POST'])
def complete_order():
    user_id = request.args.get('user_id')
    order_id = request.args.get('order_id')
    delivery_address = request.args.get('address', "123 Example St, City, Country")

    if not user_id or not order_id:
        return jsonify({"message": "User ID and Order ID are required", "success": False}), 400

    query = "UPDATE orders SET status = 'Completed' WHERE order_id = %s AND user_id = %s"
    data = (order_id, user_id)

    connection = connectToMySQL('gastroglide')
    result = connection.query_db(query, data)

    if result:
        return render_template('delivery_status.html', delivery_address=delivery_address)
    else:
        return jsonify({"message": "Failed to complete order", "success": False}), 500
