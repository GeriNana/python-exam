from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from flask_app.models.order import Order
from flask_app.models.user import User
import requests
from flask_app.config.mysqlconnection import connectToMySQL

bp = Blueprint('orders', __name__)

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

def insert_order(user_id, total):
    query = "INSERT INTO orders (user_id, total_price) VALUES (%s, %s)"
    data = (user_id, total)

    connection = connectToMySQL('gastroglide')
    result = connection.query_db(query, data)

    return result

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

def insert_order(user_id, total):
    query = "INSERT INTO orders (user_id, total_price) VALUES (%s, %s)"
    data = (user_id, total)

    connection = connectToMySQL('gastroglide')
    result = connection.query_db(query, data)

    return result

@bp.route('/checkout', methods=['GET'])
def checkout():
    return render_template('checkout.html')

@bp.route('/paypal/complete', methods=['GET', 'POST'])
def complete_order():
    user_id = request.args.get('user_id')
    order_id = request.args.get('order_id')

    if not user_id or not order_id:
        return jsonify({"message": "User ID and Order ID are required", "success": False}), 400

    query = "UPDATE orders SET status = 'Completed' WHERE order_id = %s AND user_id = %s"
    data = (order_id, user_id)

    connection = connectToMySQL('gastroglide')
    result = connection.query_db(query, data)

    if result:
        return jsonify({"message": "Order completed successfully", "success": True})
    else:
        return jsonify({"message": "Failed to complete order", "success": False}), 500

@bp.route('/paypal', methods=['POST'])
def paypal():
    user_id = request.form.get('user_id')
    total = request.form.get('total')

    if not user_id or not total:
        return jsonify({"message": "User ID and Total are required", "success": False}), 400

    payment_response = process_paypal_payment(total)

    if not payment_response['success']:
        return jsonify({"message": "Payment failed", "success": False}), 400

    order_id = insert_order(user_id, total)

    if not order_id:
        return jsonify({"message": "Failed to create order", "success": False}), 500

    return jsonify({"message": "Payment processed successfully", "order_id": order_id, "success": True})