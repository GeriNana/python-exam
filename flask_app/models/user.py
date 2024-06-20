from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.order import Order
from flask import flash

class User:
    db_name = "gastroglide"

    def __init__(self, data):
        self.id = data.get('user_id')
        self.username = data.get('username')
        self.password = data.get('password')
        self.email = data.get('email')
        self.full_name = data.get('full_name')
        self.address = data.get('address')
        self.city = data.get('city')
        self.postal_code = data.get('postal_code')
        self.phone = data.get('phone')
        self.preferred_payment_method = data.get('preferred_payment_method')

    @classmethod
    def get_user_by_id(cls, user_id):
        query = "SELECT * FROM users WHERE user_id = %(user_id)s;"
        result = connectToMySQL(cls.db_name).query_db(query, {'user_id': user_id})
        if result:
            user = cls(result[0])
            user.past_orders = Order.get_by_user_id(user_id)
            return user
        return None

    @classmethod
    def get_by_email(cls, email):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(cls.db_name).query_db(query, {'email': email})
        if result:
            return cls(result[0])
        return None

    @classmethod
    def save(cls, data):
        query = """
        INSERT INTO users (username, full_name, email, password)
        VALUES (%(username)s, %(full_name)s, %(email)s, %(password)s);
        """
        return connectToMySQL(cls.db_name).query_db(query, data)

    @staticmethod
    def validate_registration(form_data):
        is_valid = True
        errors = []

        if len(form_data['username']) < 2:
            is_valid = False
            errors.append("Username must be at least 2 characters.")

        if len(form_data['full_name']) < 2:
            is_valid = False
            errors.append("Full name must be at least 2 characters.")

        if 'email' not in form_data or not form_data['email']:
            is_valid = False
            errors.append("Email is required.")
        else:
            email_query = "SELECT * FROM users WHERE email = %(email)s;"
            email_data = {"email": form_data['email']}
            email_results = connectToMySQL('gastroglide').query_db(email_query, email_data)
            if len(email_results) > 0:
                is_valid = False
                errors.append("Email is already in use.")

        if 'password' not in form_data or not form_data['password']:
            is_valid = False
            errors.append("Password is required.")

        if not is_valid:
            for error in errors:
                flash(error, 'register')

        return is_valid


