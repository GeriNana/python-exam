from flask import Blueprint, request, render_template, redirect, url_for, jsonify
from flask_app.models.order_item import OrderItem

bp = Blueprint('orders', __name__, url_prefix='/orders')

@bp.route('/checkout', methods=['GET'])
def checkout():
    return render_template('payment_options.html')

@bp.route('/complete', methods=['POST'])
def complete_order():
    data = request.get_json()
    order_id = 1  # This should be dynamically generated or fetched based on the current order context
    method = data.get('method')
    basket = data.get('basket')
    success = True

    for dish_name, details in basket.items():
        order_item_data = {
            'order_id': order_id,
            'menu_id': 1,  # This should be fetched or passed correctly based on the dish context
            'quantity': details['quantity'],
            'price': details['price']
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
