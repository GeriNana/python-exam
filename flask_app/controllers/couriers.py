from flask import Blueprint, render_template, redirect, request, session, flash
from flask_app.models.courier import Courier
from flask_app.models.courier_application import CourierApplication

bp = Blueprint('couriers', __name__)

@bp.route('/apply', methods=['GET', 'POST'])
def apply():
    if request.method == 'POST':
        data = {
            "full_name": request.form["full_name"],
            "email": request.form["email"],
            "phone": request.form["phone"],
            "address": request.form["address"],
            "city": request.form["city"],
            "postal_code": request.form["postal_code"],
            "vehicle_type": request.form["vehicle_type"]
        }
        CourierApplication.save(data)
        return redirect('/')
    return render_template('apply.html')

@bp.route('/create_courier', methods=['POST'])
def create_courier():
    data = {
        "full_name": request.form["full_name"],
        "email": request.form["email"],
        "phone": request.form["phone"],
        "address": request.form["address"],
        "city": request.form["city"],
        "postal_code": request.form["postal_code"],
        "vehicle_type": request.form["vehicle_type"]
    }
    Courier.save(data)
    return redirect('/')
