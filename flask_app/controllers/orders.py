from flask import Blueprint, request, render_template, redirect, url_for, session, flash, jsonify
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.order import Order
import requests
from flask_app.models.order_item import OrderItem
from flask_app.models.user import get_user_by_id
import datetime

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

@orders_bp.route('/add_to_basket', methods=['POST'])
def add_to_basket():
    if 'user_id' not in session:
        flash("You must be logged in to order.", "error")
        return redirect(url_for('users.login'))

    user_id = session['user_id']
    dish_id = request.form.get('dish_id')
    menu_id = request.form.get('menu_id')
    price = request.form.get('price')

    if not dish_id or not menu_id or not price:
        flash("Invalid order request.", "error")
        return redirect(request.referrer)

    # Ensure the restaurant_id exists
    query = "SELECT restaurant_id FROM menus WHERE id = %(menu_id)s"
    result = connectToMySQL('gastroglide').query_db(query, {'menu_id': menu_id})
    if not result:
        flash("Invalid menu or restaurant ID.", "error")
        return redirect(request.referrer)
    
    restaurant_id = result[0]['restaurant_id']

    order_id = session.get('order_id')

    if not order_id:
        order_data = {
            'user_id': user_id,
            'restaurant_id': restaurant_id,
            'order_date': datetime.datetime.now(),
            'delivery_address': '',  # Will be filled in later
            'city': '',  # Will be filled in later
            'postal_code': '',  # Will be filled in later
            'phone': '',  # Will be filled in later
            'total_price': 0.0,  # Will be calculated later
            'payment_method': 'Cash on Delivery',  # Default, will be updated later
            'status': 'Pending'
        }
        order_id = Order.save(order_data)
        session['order_id'] = order_id

    order_item_data = {
        'order_id': order_id,
        'menu_id': menu_id,
        'dish_id': dish_id,
        'quantity': 1,  # Default quantity
        'price': price
    }
    OrderItem.save(order_item_data)
    flash("Item added to basket!", "success")
    return redirect(request.referrer)

@orders_bp.route('/view_basket', methods=['GET'])
def view_basket():
    if 'user_id' not in session:
        flash("You must be logged in to view your basket.", "error")
        return redirect(url_for('users.login'))

    order_id = session.get('order_id')
    if not order_id:
        flash("Your basket is empty.", "error")
        return redirect(url_for('menus.show_menu'))

    order_items = OrderItem.get_by_order_id(order_id)
    total_price = sum(item.price * item.quantity for item in order_items)

    return render_template('basket.html', order_items=order_items, total_price=total_price)

@orders_bp.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if 'user_id' in session:
        user_id = session['user_id']
        user_data = get_user_by_id(user_id)
        order_id = session.get('order_id')
        total_price = 0.0

        if order_id:
            order_items = OrderItem.get_by_order_id(order_id)
            total_price = sum(item.price * item.quantity for item in order_items)

        return render_template('checkout.html', user_logged_in=True, user_address=user_data.address,
                               user_postal_code=user_data.postal_code, user_phone=user_data.phone,
                               total_price=total_price, order_id=order_id, restaurant_id=order_items[0].menu_id if order_items else None)
    else:
        if request.method == 'POST':
            restaurant_id = request.form['restaurant_id']
            order_id = request.form['order_id']
            total_price = request.form['total_price']
            payment_method = request.form['payment_method']
            address = request.form['address']
            postal_code = request.form['postal_code']
            phone = request.form['phone']

            order_data = {
                'user_id': None,  # Handle anonymous user
                'restaurant_id': restaurant_id,
                'order_date': datetime.datetime.now(),
                'delivery_address': address,
                'city': '',  # Will be filled in later
                'postal_code': postal_code,
                'phone': phone,
                'total_price': total_price,
                'payment_method': payment_method,
                'status': 'Pending'
            }
            order_id = Order.save(order_data)
            flash('Order placed successfully!', 'success')
            return redirect(url_for('orders.delivery_status', order_id=order_id))

        return render_template('checkout.html', user_logged_in=False, total_price=0.0)

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

    order_data = {
        'user_id': user_id,
        'restaurant_id': restaurant_id,
        'order_date': datetime.datetime.now(),
        'delivery_address': address,
        'city': '',  # Will be filled in later
        'postal_code': postal_code,
        'phone': phone,
        'total_price': total_price,
        'payment_method': payment_method,
        'status': 'Pending'
    }
    order_id = Order.save(order_data)

    flash('Order placed successfully!', 'success')
    return render_template('delivery_status.html', delivery_address=address)

@orders_bp.route('/delivery_status')
def delivery_status():
    return render_template('delivery_status.html')

@orders_bp.route('/past_orders/<int:user_id>')
def past_orders(user_id):
    orders = Order.get_by_user_id(user_id)
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
