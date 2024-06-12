import os
from flask import Flask, render_template, redirect, request, url_for, jsonify
from flask_app.controllers import users, restaurants, menus, couriers, dishes, favorites
from flask_app.controllers.orders import bp as orders_bp
import paypalrestsdk

app = Flask(__name__, template_folder='flask_app/templates', static_folder='flask_app/static')
app.secret_key = 'your_secret_key'  # Change this to a real secret key

paypalrestsdk.configure({
  "mode": "sandbox",  # sandbox or live
  "client_id": "AYQr6DtNYss6xFtKkIpjSBOfctFCX2YEWOCFTxR1Vti0-vef9mBTnLsQnhPO9NADU35AO3p9NM0sWski",
  "client_secret": "EFTO8utZsrDsBhj_PO8zVtgv5rMmCyKLzzE31bej56WO9v9B3VR4QdKMrnL4YZDBmIeheMEByZ3QxZrv"
})

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/pay', methods=['POST'])
def pay():
    user_id = request.form.get('user_id')
    total = request.form.get('total')

    if not user_id or not total:
        return jsonify({"message": "User ID and Total are required", "success": False}), 400

    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"},
        "redirect_urls": {
            "return_url": url_for('payment_execute', _external=True),
            "cancel_url": url_for('payment_cancel', _external=True)},
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": "Order Total",
                    "sku": "item",
                    "price": total,
                    "currency": "USD",
                    "quantity": 1}]},
            "amount": {
                "total": total,
                "currency": "USD"},
            "description": "Payment for your order"}]})

    if payment.create():
        for link in payment.links:
            if link.rel == "approval_url":
                approval_url = link.href
                return jsonify({"success": True, "approval_url": approval_url})
    else:
        return jsonify({"message": "Payment failed", "success": False}), 400

@app.route('/payment/execute', methods=['GET'])
def payment_execute():
    payment = paypalrestsdk.Payment.find(request.args.get('paymentId'))

    if payment.execute({"payer_id": request.args.get('PayerID')}):
        return render_template('payment_success.html')
    else:
        return render_template('payment_error.html', error=payment.error)

@app.route('/payment/cancel', methods=['GET'])
def payment_cancel():
    return render_template('payment_cancel.html')

# Register the blueprints or controllers
app.register_blueprint(users.bp, url_prefix='/users')
app.register_blueprint(restaurants.bp, url_prefix='/restaurants')
app.register_blueprint(menus.bp, url_prefix='/menus')
app.register_blueprint(orders_bp, url_prefix='/orders')
app.register_blueprint(favorites.bp, url_prefix='/favorites')
app.register_blueprint(couriers.bp, url_prefix='/couriers')
app.register_blueprint(dishes.bp, url_prefix='/dishes')

if __name__ == "__main__":
    app.run(debug=True)
