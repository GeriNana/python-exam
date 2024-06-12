from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.order_item import OrderItem
from flask_app.models.favorite import Favorite
from flask import flash
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

class User:
    db_name = "gastroglide"

    def __init__(self, data):
        self.id = data['user_id']
        self.username = data['username']
        self.full_name = data['full_name']
        self.email = data['email']
        self.password = data['password']
        self.past_orders = []
        self.favorites = []

    @classmethod
    def save(cls, data):
        hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        data['password'] = hashed_password
        query = """
        INSERT INTO users (username, full_name, email, password)
        VALUES (%(username)s, %(full_name)s, %(email)s, %(password)s);
        """
        user_id = connectToMySQL(cls.db_name).query_db(query, data)
        return user_id

    @classmethod
    def get_by_id(cls, user_id):
        query = "SELECT * FROM users WHERE user_id = %(user_id)s;"
        print(f"Running Query: {query} with user_id: {user_id}")
        result = connectToMySQL(cls.db_name).query_db(query, {"user_id": user_id})
        if result:
            user_data = result[0]
            print(f"User found: {user_data}")
            user = cls(user_data)
            user.past_orders = OrderItem.get_by_user_id(user_id)
            user.favorites = Favorite.get_by_user_id(user_id)
            return user
        else:
            print("User not found")
        return None

    @classmethod
    def get_by_email(cls, email):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(cls.db_name).query_db(query, {"email": email})
        if result:
            return cls(result[0])
        return None

    def check_password(self, password):
        return self.password == password
    
    @classmethod
    def get_by_user_id(cls, user_id):
        query = """
        SELECT o.order_id, o.user_id, r.name AS restaurant_name, o.order_date, o.total_price,
            GROUP_CONCAT(d.name SEPARATOR ', ') AS dishes
        FROM orders o
        JOIN restaurants r ON o.restaurant_id = r.restaurant_id
        JOIN order_items oi ON o.order_id = oi.order_id
        JOIN dishes d ON oi.menu_id = d.menu_id
        WHERE o.user_id = %(user_id)s
        GROUP BY o.order_id;
        """
        results = connectToMySQL(cls.db_name).query_db(query, {"user_id": user_id})
        return [cls(row) for row in results] if results else []

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
