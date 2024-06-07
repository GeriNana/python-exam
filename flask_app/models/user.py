from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
from flask_bcrypt import Bcrypt
from flask_app import app

bcrypt = Bcrypt(app)

class User:
    def __init__(self, data):
        self.id = data['user_id']
        self.username = data['username']
        self.password = data['password']
        self.email = data['email']
        self.full_name = data.get('full_name')
        self.address = data.get('address')
        self.city = data.get('city')
        self.postal_code = data.get('postal_code')
        self.phone = data.get('phone')
        self.preferred_payment_method = data.get('preferred_payment_method')

    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (username, password, email, full_name, address, city, postal_code, phone) VALUES (%(username)s, %(password)s, %(email)s, %(full_name)s, %(address)s, %(city)s, %(postal_code)s, %(phone)s);"
        return connectToMySQL('gastroglide').query_db(query, data)

    @classmethod
    def get_by_email(cls, email):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL('gastroglide').query_db(query, {'email': email})
        if not result:
            return None
        return cls(result[0])

    @staticmethod
    def validate_registration(form_data):
        is_valid = True
        if len(form_data['username']) < 3:
            flash("Username must be at least 3 characters.", "register")
            is_valid = False
        if len(form_data['password']) < 8:
            flash("Password must be at least 8 characters.", "register")
            is_valid = False
        if not re.match(r"[^@]+@[^@]+\.[^@]+", form_data['email']):
            flash("Invalid email address.", "register")
            is_valid = False
        if User.get_by_email(form_data['email']):
            flash("Email already taken.", "register")
            is_valid = False
        return is_valid


    @classmethod
    def check_password(cls, stored_password, provided_password):
        return stored_password == provided_password

    @classmethod
    def get_by_id(cls, user_id):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        data = {'id': user_id}
        result = connectToMySQL('gastroglide').query_db(query, data)
        if not result:
            return None
        return cls(result[0])
