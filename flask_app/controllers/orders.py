from flask import Blueprint, request, jsonify, session, render_template, redirect, url_for
from flask_app.models.order_item import OrderItem
from flask_app.models.order import Order

bp = Blueprint('orders', __name__, url_prefix='/orders')

@bp.route('/checkout', methods=['GET'])
def checkout():
    if 'user_id' not in session:
        return redirect('/users/login')
    return render_template('payment_options.html')

@bp.route('/complete', methods=['POST'])
def complete_order():
    if 'user_id' not in session:
        return redirect('/users/login')

    data = request.get_json()
    user_id = session['user_id']
    order_id = data.get('order_id')  # Assume order_id is generated properly
    basket = data.get('basket')
    success = True

    # Save the order details
    order_data = {
        'user_id': user_id,
        'restaurant_id': data.get('restaurant_id'),
        'order_date': data.get('order_date'),
        'delivery_address': data.get('delivery_address'),
        'city': data.get('city'),
        'postal_code': data.get('postal_code'),
        'phone': data.get('phone'),
        'total_price': data.get('total_price'),
        'payment_method': data.get('payment_method'),
        'status': data.get('status')
    }
    result = Order.save(order_data)
    if not result:
        success = False

    # Save order items
    for dish_name, details in basket.items():
        order_item_data = {
            'order_id': order_id,
            'menu_id': details['menu_id'],
            'quantity': details['quantity'],
            'price': details['price'],
            'user_id': user_id
        }
        result = OrderItem.save(order_item_data)
        if not result:
            success = False

    return jsonify({'success': success})

@bp.route('/paypal', methods=['POST'])
def paypal():
    total = request.form['total']
    # Here, integrate with PayPal's API for payment processing
    return redirect(url_for('orders.paypal_complete'))

@bp.route('/paypal/complete', methods=['GET'])
def paypal_complete():
    # Handle post-PayPal payment success logic here
    return "PayPal payment successful!"
